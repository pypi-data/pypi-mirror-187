do
local _ENV = _ENV
package.preload[ "dkjson" ] = function( ... ) local arg = _G.arg;
-- Module options:
local always_use_lpeg = false
local register_global_module_table = false
local global_module_name = 'json'

--[==[

David Kolf's JSON module for Lua 5.1 - 5.4

Version 2.6


For the documentation see the corresponding readme.txt or visit
<http://dkolf.de/src/dkjson-lua.fsl/>.

You can contact the author by sending an e-mail to 'david' at the
domain 'dkolf.de'.


Copyright (C) 2010-2021 David Heiko Kolf

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

--]==]

-- global dependencies:
local pairs, type, tostring, tonumber, getmetatable, setmetatable, rawset =
      pairs, type, tostring, tonumber, getmetatable, setmetatable, rawset
local error, require, pcall, select = error, require, pcall, select
local floor, huge = math.floor, math.huge
local strrep, gsub, strsub, strbyte, strchar, strfind, strlen, strformat =
      string.rep, string.gsub, string.sub, string.byte, string.char,
      string.find, string.len, string.format
local strmatch = string.match
local concat = table.concat

local json = { version = "dkjson 2.6" }

local jsonlpeg = {}

if register_global_module_table then
  if always_use_lpeg then
    _G[global_module_name] = jsonlpeg
  else
    _G[global_module_name] = json
  end
end

local _ENV = nil -- blocking globals in Lua 5.2 and later

pcall (function()
  -- Enable access to blocked metatables.
  -- Don't worry, this module doesn't change anything in them.
  local debmeta = require "debug".getmetatable
  if debmeta then getmetatable = debmeta end
end)

json.null = setmetatable ({}, {
  __tojson = function () return "null" end
})

local function isarray (tbl)
  local max, n, arraylen = 0, 0, 0
  for k,v in pairs (tbl) do
    if k == 'n' and type(v) == 'number' then
      arraylen = v
      if v > max then
        max = v
      end
    else
      if type(k) ~= 'number' or k < 1 or floor(k) ~= k then
        return false
      end
      if k > max then
        max = k
      end
      n = n + 1
    end
  end
  if max > 10 and max > arraylen and max > n * 2 then
    return false -- don't create an array with too many holes
  end
  return true, max
end

local escapecodes = {
  ["\""] = "\\\"", ["\\"] = "\\\\", ["\b"] = "\\b", ["\f"] = "\\f",
  ["\n"] = "\\n",  ["\r"] = "\\r",  ["\t"] = "\\t"
}

local function escapeutf8 (uchar)
  local value = escapecodes[uchar]
  if value then
    return value
  end
  local a, b, c, d = strbyte (uchar, 1, 4)
  a, b, c, d = a or 0, b or 0, c or 0, d or 0
  if a <= 0x7f then
    value = a
  elseif 0xc0 <= a and a <= 0xdf and b >= 0x80 then
    value = (a - 0xc0) * 0x40 + b - 0x80
  elseif 0xe0 <= a and a <= 0xef and b >= 0x80 and c >= 0x80 then
    value = ((a - 0xe0) * 0x40 + b - 0x80) * 0x40 + c - 0x80
  elseif 0xf0 <= a and a <= 0xf7 and b >= 0x80 and c >= 0x80 and d >= 0x80 then
    value = (((a - 0xf0) * 0x40 + b - 0x80) * 0x40 + c - 0x80) * 0x40 + d - 0x80
  else
    return ""
  end
  if value <= 0xffff then
    return strformat ("\\u%.4x", value)
  elseif value <= 0x10ffff then
    -- encode as UTF-16 surrogate pair
    value = value - 0x10000
    local highsur, lowsur = 0xD800 + floor (value/0x400), 0xDC00 + (value % 0x400)
    return strformat ("\\u%.4x\\u%.4x", highsur, lowsur)
  else
    return ""
  end
end

local function fsub (str, pattern, repl)
  -- gsub always builds a new string in a buffer, even when no match
  -- exists. First using find should be more efficient when most strings
  -- don't contain the pattern.
  if strfind (str, pattern) then
    return gsub (str, pattern, repl)
  else
    return str
  end
end

local function quotestring (value)
  -- based on the regexp "escapable" in https://github.com/douglascrockford/JSON-js
  value = fsub (value, "[%z\1-\31\"\\\127]", escapeutf8)
  if strfind (value, "[\194\216\220\225\226\239]") then
    value = fsub (value, "\194[\128-\159\173]", escapeutf8)
    value = fsub (value, "\216[\128-\132]", escapeutf8)
    value = fsub (value, "\220\143", escapeutf8)
    value = fsub (value, "\225\158[\180\181]", escapeutf8)
    value = fsub (value, "\226\128[\140-\143\168-\175]", escapeutf8)
    value = fsub (value, "\226\129[\160-\175]", escapeutf8)
    value = fsub (value, "\239\187\191", escapeutf8)
    value = fsub (value, "\239\191[\176-\191]", escapeutf8)
  end
  return "\"" .. value .. "\""
end
json.quotestring = quotestring

local function replace(str, o, n)
  local i, j = strfind (str, o, 1, true)
  if i then
    return strsub(str, 1, i-1) .. n .. strsub(str, j+1, -1)
  else
    return str
  end
end

-- locale independent num2str and str2num functions
local decpoint, numfilter

local function updatedecpoint ()
  decpoint = strmatch(tostring(0.5), "([^05+])")
  -- build a filter that can be used to remove group separators
  numfilter = "[^0-9%-%+eE" .. gsub(decpoint, "[%^%$%(%)%%%.%[%]%*%+%-%?]", "%%%0") .. "]+"
end

updatedecpoint()

local function num2str (num)
  return replace(fsub(tostring(num), numfilter, ""), decpoint, ".")
end

local function str2num (str)
  local num = tonumber(replace(str, ".", decpoint))
  if not num then
    updatedecpoint()
    num = tonumber(replace(str, ".", decpoint))
  end
  return num
end

local function addnewline2 (level, buffer, buflen)
  buffer[buflen+1] = "\n"
  buffer[buflen+2] = strrep ("  ", level)
  buflen = buflen + 2
  return buflen
end

function json.addnewline (state)
  if state.indent then
    state.bufferlen = addnewline2 (state.level or 0,
                           state.buffer, state.bufferlen or #(state.buffer))
  end
end

local encode2 -- forward declaration

local function addpair (key, value, prev, indent, level, buffer, buflen, tables, globalorder, state)
  local kt = type (key)
  if kt ~= 'string' and kt ~= 'number' then
    return nil, "type '" .. kt .. "' is not supported as a key by JSON."
  end
  if prev then
    buflen = buflen + 1
    buffer[buflen] = ","
  end
  if indent then
    buflen = addnewline2 (level, buffer, buflen)
  end
  buffer[buflen+1] = quotestring (key)
  buffer[buflen+2] = ":"
  return encode2 (value, indent, level, buffer, buflen + 2, tables, globalorder, state)
end

local function appendcustom(res, buffer, state)
  local buflen = state.bufferlen
  if type (res) == 'string' then
    buflen = buflen + 1
    buffer[buflen] = res
  end
  return buflen
end

local function exception(reason, value, state, buffer, buflen, defaultmessage)
  defaultmessage = defaultmessage or reason
  local handler = state.exception
  if not handler then
    return nil, defaultmessage
  else
    state.bufferlen = buflen
    local ret, msg = handler (reason, value, state, defaultmessage)
    if not ret then return nil, msg or defaultmessage end
    return appendcustom(ret, buffer, state)
  end
end

function json.encodeexception(reason, value, state, defaultmessage)
  return quotestring("<" .. defaultmessage .. ">")
end

encode2 = function (value, indent, level, buffer, buflen, tables, globalorder, state)
  local valtype = type (value)
  local valmeta = getmetatable (value)
  valmeta = type (valmeta) == 'table' and valmeta -- only tables
  local valtojson = valmeta and valmeta.__tojson
  if valtojson then
    if tables[value] then
      return exception('reference cycle', value, state, buffer, buflen)
    end
    tables[value] = true
    state.bufferlen = buflen
    local ret, msg = valtojson (value, state)
    if not ret then return exception('custom encoder failed', value, state, buffer, buflen, msg) end
    tables[value] = nil
    buflen = appendcustom(ret, buffer, state)
  elseif value == nil then
    buflen = buflen + 1
    buffer[buflen] = "null"
  elseif valtype == 'number' then
    local s
    if value ~= value or value >= huge or -value >= huge then
      -- This is the behaviour of the original JSON implementation.
      s = "null"
    else
      s = num2str (value)
    end
    buflen = buflen + 1
    buffer[buflen] = s
  elseif valtype == 'boolean' then
    buflen = buflen + 1
    buffer[buflen] = value and "true" or "false"
  elseif valtype == 'string' then
    buflen = buflen + 1
    buffer[buflen] = quotestring (value)
  elseif valtype == 'table' then
    if tables[value] then
      return exception('reference cycle', value, state, buffer, buflen)
    end
    tables[value] = true
    level = level + 1
    local isa, n = isarray (value)
    if n == 0 and valmeta and valmeta.__jsontype == 'object' then
      isa = false
    end
    local msg
    if isa then -- JSON array
      buflen = buflen + 1
      buffer[buflen] = "["
      for i = 1, n do
        buflen, msg = encode2 (value[i], indent, level, buffer, buflen, tables, globalorder, state)
        if not buflen then return nil, msg end
        if i < n then
          buflen = buflen + 1
          buffer[buflen] = ","
        end
      end
      buflen = buflen + 1
      buffer[buflen] = "]"
    else -- JSON object
      local prev = false
      buflen = buflen + 1
      buffer[buflen] = "{"
      local order = valmeta and valmeta.__jsonorder or globalorder
      if order then
        local used = {}
        n = #order
        for i = 1, n do
          local k = order[i]
          local v = value[k]
          if v ~= nil then
            used[k] = true
            buflen, msg = addpair (k, v, prev, indent, level, buffer, buflen, tables, globalorder, state)
            prev = true -- add a seperator before the next element
          end
        end
        for k,v in pairs (value) do
          if not used[k] then
            buflen, msg = addpair (k, v, prev, indent, level, buffer, buflen, tables, globalorder, state)
            if not buflen then return nil, msg end
            prev = true -- add a seperator before the next element
          end
        end
      else -- unordered
        for k,v in pairs (value) do
          buflen, msg = addpair (k, v, prev, indent, level, buffer, buflen, tables, globalorder, state)
          if not buflen then return nil, msg end
          prev = true -- add a seperator before the next element
        end
      end
      if indent then
        buflen = addnewline2 (level - 1, buffer, buflen)
      end
      buflen = buflen + 1
      buffer[buflen] = "}"
    end
    tables[value] = nil
  else
    return exception ('unsupported type', value, state, buffer, buflen,
      "type '" .. valtype .. "' is not supported by JSON.")
  end
  return buflen
end

function json.encode (value, state)
  state = state or {}
  local oldbuffer = state.buffer
  local buffer = oldbuffer or {}
  state.buffer = buffer
  updatedecpoint()
  local ret, msg = encode2 (value, state.indent, state.level or 0,
                   buffer, state.bufferlen or 0, state.tables or {}, state.keyorder, state)
  if not ret then
    error (msg, 2)
  elseif oldbuffer == buffer then
    state.bufferlen = ret
    return true
  else
    state.bufferlen = nil
    state.buffer = nil
    return concat (buffer)
  end
end

local function loc (str, where)
  local line, pos, linepos = 1, 1, 0
  while true do
    pos = strfind (str, "\n", pos, true)
    if pos and pos < where then
      line = line + 1
      linepos = pos
      pos = pos + 1
    else
      break
    end
  end
  return "line " .. line .. ", column " .. (where - linepos)
end

local function unterminated (str, what, where)
  return nil, strlen (str) + 1, "unterminated " .. what .. " at " .. loc (str, where)
end

local function scanwhite (str, pos)
  while true do
    pos = strfind (str, "%S", pos)
    if not pos then return nil end
    local sub2 = strsub (str, pos, pos + 1)
    if sub2 == "\239\187" and strsub (str, pos + 2, pos + 2) == "\191" then
      -- UTF-8 Byte Order Mark
      pos = pos + 3
    elseif sub2 == "//" then
      pos = strfind (str, "[\n\r]", pos + 2)
      if not pos then return nil end
    elseif sub2 == "/*" then
      pos = strfind (str, "*/", pos + 2)
      if not pos then return nil end
      pos = pos + 2
    else
      return pos
    end
  end
end

local escapechars = {
  ["\""] = "\"", ["\\"] = "\\", ["/"] = "/", ["b"] = "\b", ["f"] = "\f",
  ["n"] = "\n", ["r"] = "\r", ["t"] = "\t"
}

local function unichar (value)
  if value < 0 then
    return nil
  elseif value <= 0x007f then
    return strchar (value)
  elseif value <= 0x07ff then
    return strchar (0xc0 + floor(value/0x40),
                    0x80 + (floor(value) % 0x40))
  elseif value <= 0xffff then
    return strchar (0xe0 + floor(value/0x1000),
                    0x80 + (floor(value/0x40) % 0x40),
                    0x80 + (floor(value) % 0x40))
  elseif value <= 0x10ffff then
    return strchar (0xf0 + floor(value/0x40000),
                    0x80 + (floor(value/0x1000) % 0x40),
                    0x80 + (floor(value/0x40) % 0x40),
                    0x80 + (floor(value) % 0x40))
  else
    return nil
  end
end

local function scanstring (str, pos)
  local lastpos = pos + 1
  local buffer, n = {}, 0
  while true do
    local nextpos = strfind (str, "[\"\\]", lastpos)
    if not nextpos then
      return unterminated (str, "string", pos)
    end
    if nextpos > lastpos then
      n = n + 1
      buffer[n] = strsub (str, lastpos, nextpos - 1)
    end
    if strsub (str, nextpos, nextpos) == "\"" then
      lastpos = nextpos + 1
      break
    else
      local escchar = strsub (str, nextpos + 1, nextpos + 1)
      local value
      if escchar == "u" then
        value = tonumber (strsub (str, nextpos + 2, nextpos + 5), 16)
        if value then
          local value2
          if 0xD800 <= value and value <= 0xDBff then
            -- we have the high surrogate of UTF-16. Check if there is a
            -- low surrogate escaped nearby to combine them.
            if strsub (str, nextpos + 6, nextpos + 7) == "\\u" then
              value2 = tonumber (strsub (str, nextpos + 8, nextpos + 11), 16)
              if value2 and 0xDC00 <= value2 and value2 <= 0xDFFF then
                value = (value - 0xD800)  * 0x400 + (value2 - 0xDC00) + 0x10000
              else
                value2 = nil -- in case it was out of range for a low surrogate
              end
            end
          end
          value = value and unichar (value)
          if value then
            if value2 then
              lastpos = nextpos + 12
            else
              lastpos = nextpos + 6
            end
          end
        end
      end
      if not value then
        value = escapechars[escchar] or escchar
        lastpos = nextpos + 2
      end
      n = n + 1
      buffer[n] = value
    end
  end
  if n == 1 then
    return buffer[1], lastpos
  elseif n > 1 then
    return concat (buffer), lastpos
  else
    return "", lastpos
  end
end

local scanvalue -- forward declaration

local function scantable (what, closechar, str, startpos, nullval, objectmeta, arraymeta)
  local len = strlen (str)
  local tbl, n = {}, 0
  local pos = startpos + 1
  if what == 'object' then
    setmetatable (tbl, objectmeta)
  else
    setmetatable (tbl, arraymeta)
  end
  while true do
    pos = scanwhite (str, pos)
    if not pos then return unterminated (str, what, startpos) end
    local char = strsub (str, pos, pos)
    if char == closechar then
      return tbl, pos + 1
    end
    local val1, err
    val1, pos, err = scanvalue (str, pos, nullval, objectmeta, arraymeta)
    if err then return nil, pos, err end
    pos = scanwhite (str, pos)
    if not pos then return unterminated (str, what, startpos) end
    char = strsub (str, pos, pos)
    if char == ":" then
      if val1 == nil then
        return nil, pos, "cannot use nil as table index (at " .. loc (str, pos) .. ")"
      end
      pos = scanwhite (str, pos + 1)
      if not pos then return unterminated (str, what, startpos) end
      local val2
      val2, pos, err = scanvalue (str, pos, nullval, objectmeta, arraymeta)
      if err then return nil, pos, err end
      tbl[val1] = val2
      pos = scanwhite (str, pos)
      if not pos then return unterminated (str, what, startpos) end
      char = strsub (str, pos, pos)
    else
      n = n + 1
      tbl[n] = val1
    end
    if char == "," then
      pos = pos + 1
    end
  end
end

scanvalue = function (str, pos, nullval, objectmeta, arraymeta)
  pos = pos or 1
  pos = scanwhite (str, pos)
  if not pos then
    return nil, strlen (str) + 1, "no valid JSON value (reached the end)"
  end
  local char = strsub (str, pos, pos)
  if char == "{" then
    return scantable ('object', "}", str, pos, nullval, objectmeta, arraymeta)
  elseif char == "[" then
    return scantable ('array', "]", str, pos, nullval, objectmeta, arraymeta)
  elseif char == "\"" then
    return scanstring (str, pos)
  else
    local pstart, pend = strfind (str, "^%-?[%d%.]+[eE]?[%+%-]?%d*", pos)
    if pstart then
      local number = str2num (strsub (str, pstart, pend))
      if number then
        return number, pend + 1
      end
    end
    pstart, pend = strfind (str, "^%a%w*", pos)
    if pstart then
      local name = strsub (str, pstart, pend)
      if name == "true" then
        return true, pend + 1
      elseif name == "false" then
        return false, pend + 1
      elseif name == "null" then
        return nullval, pend + 1
      end
    end
    return nil, pos, "no valid JSON value at " .. loc (str, pos)
  end
end

local function optionalmetatables(...)
  if select("#", ...) > 0 then
    return ...
  else
    return {__jsontype = 'object'}, {__jsontype = 'array'}
  end
end

function json.decode (str, pos, nullval, ...)
  local objectmeta, arraymeta = optionalmetatables(...)
  return scanvalue (str, pos, nullval, objectmeta, arraymeta)
end

function json.use_lpeg ()
  local g = require ("lpeg")

  if g.version() == "0.11" then
    error "due to a bug in LPeg 0.11, it cannot be used for JSON matching"
  end

  local pegmatch = g.match
  local P, S, R = g.P, g.S, g.R

  local function ErrorCall (str, pos, msg, state)
    if not state.msg then
      state.msg = msg .. " at " .. loc (str, pos)
      state.pos = pos
    end
    return false
  end

  local function Err (msg)
    return g.Cmt (g.Cc (msg) * g.Carg (2), ErrorCall)
  end

  local function ErrorUnterminatedCall (str, pos, what, state)
    return ErrorCall (str, pos - 1, "unterminated " .. what, state)
  end

  local SingleLineComment = P"//" * (1 - S"\n\r")^0
  local MultiLineComment = P"/*" * (1 - P"*/")^0 * P"*/"
  local Space = (S" \n\r\t" + P"\239\187\191" + SingleLineComment + MultiLineComment)^0

  local function ErrUnterminated (what)
    return g.Cmt (g.Cc (what) * g.Carg (2), ErrorUnterminatedCall)
  end

  local PlainChar = 1 - S"\"\\\n\r"
  local EscapeSequence = (P"\\" * g.C (S"\"\\/bfnrt" + Err "unsupported escape sequence")) / escapechars
  local HexDigit = R("09", "af", "AF")
  local function UTF16Surrogate (match, pos, high, low)
    high, low = tonumber (high, 16), tonumber (low, 16)
    if 0xD800 <= high and high <= 0xDBff and 0xDC00 <= low and low <= 0xDFFF then
      return true, unichar ((high - 0xD800)  * 0x400 + (low - 0xDC00) + 0x10000)
    else
      return false
    end
  end
  local function UTF16BMP (hex)
    return unichar (tonumber (hex, 16))
  end
  local U16Sequence = (P"\\u" * g.C (HexDigit * HexDigit * HexDigit * HexDigit))
  local UnicodeEscape = g.Cmt (U16Sequence * U16Sequence, UTF16Surrogate) + U16Sequence/UTF16BMP
  local Char = UnicodeEscape + EscapeSequence + PlainChar
  local String = P"\"" * (g.Cs (Char ^ 0) * P"\"" + ErrUnterminated "string")
  local Integer = P"-"^(-1) * (P"0" + (R"19" * R"09"^0))
  local Fractal = P"." * R"09"^0
  local Exponent = (S"eE") * (S"+-")^(-1) * R"09"^1
  local Number = (Integer * Fractal^(-1) * Exponent^(-1))/str2num
  local Constant = P"true" * g.Cc (true) + P"false" * g.Cc (false) + P"null" * g.Carg (1)
  local SimpleValue = Number + String + Constant
  local ArrayContent, ObjectContent

  -- The functions parsearray and parseobject parse only a single value/pair
  -- at a time and store them directly to avoid hitting the LPeg limits.
  local function parsearray (str, pos, nullval, state)
    local obj, cont
    local start = pos
    local npos
    local t, nt = {}, 0
    repeat
      obj, cont, npos = pegmatch (ArrayContent, str, pos, nullval, state)
      if cont == 'end' then
        return ErrorUnterminatedCall (str, start, "array", state)
      end
      pos = npos
      if cont == 'cont' or cont == 'last' then
        nt = nt + 1
        t[nt] = obj
      end
    until cont ~= 'cont'
    return pos, setmetatable (t, state.arraymeta)
  end

  local function parseobject (str, pos, nullval, state)
    local obj, key, cont
    local start = pos
    local npos
    local t = {}
    repeat
      key, obj, cont, npos = pegmatch (ObjectContent, str, pos, nullval, state)
      if cont == 'end' then
        return ErrorUnterminatedCall (str, start, "object", state)
      end
      pos = npos
      if cont == 'cont' or cont == 'last' then
        t[key] = obj
      end
    until cont ~= 'cont'
    return pos, setmetatable (t, state.objectmeta)
  end

  local Array = P"[" * g.Cmt (g.Carg(1) * g.Carg(2), parsearray)
  local Object = P"{" * g.Cmt (g.Carg(1) * g.Carg(2), parseobject)
  local Value = Space * (Array + Object + SimpleValue)
  local ExpectedValue = Value + Space * Err "value expected"
  local ExpectedKey = String + Err "key expected"
  local End = P(-1) * g.Cc'end'
  local ErrInvalid = Err "invalid JSON"
  ArrayContent = (Value * Space * (P"," * g.Cc'cont' + P"]" * g.Cc'last'+ End + ErrInvalid)  + g.Cc(nil) * (P"]" * g.Cc'empty' + End  + ErrInvalid)) * g.Cp()
  local Pair = g.Cg (Space * ExpectedKey * Space * (P":" + Err "colon expected") * ExpectedValue)
  ObjectContent = (g.Cc(nil) * g.Cc(nil) * P"}" * g.Cc'empty' + End + (Pair * Space * (P"," * g.Cc'cont' + P"}" * g.Cc'last' + End + ErrInvalid) + ErrInvalid)) * g.Cp()
  local DecodeValue = ExpectedValue * g.Cp ()

  jsonlpeg.version = json.version
  jsonlpeg.encode = json.encode
  jsonlpeg.null = json.null
  jsonlpeg.quotestring = json.quotestring
  jsonlpeg.addnewline = json.addnewline
  jsonlpeg.encodeexception = json.encodeexception
  jsonlpeg.using_lpeg = true

  function jsonlpeg.decode (str, pos, nullval, ...)
    local state = {}
    state.objectmeta, state.arraymeta = optionalmetatables(...)
    local obj, retpos = pegmatch (DecodeValue, str, pos, nullval, state)
    if state.msg then
      return nil, state.pos, state.msg
    else
      return obj, retpos
    end
  end

  -- cache result of this function:
  json.use_lpeg = function () return jsonlpeg end
  jsonlpeg.use_lpeg = json.use_lpeg

  return jsonlpeg
end

if always_use_lpeg then
  return json.use_lpeg()
end

return json
end
end

do
local _ENV = _ENV
package.preload[ "src.csv" ] = function( ... ) local arg = _G.arg;
local Writer = {}
function Writer:new(fields)
  self.__index = self
  return setmetatable({
    header = table.concat(fields, ','),
    columns = #fields,
    data = "",
  }, self)
end

local function quoted(string)
  return '"' .. tostring(string):gsub('"', '""') .. '"'
end

function Writer:record(fields)
  -- Create CSV record.
  if #fields ~= self.columns then
    error(string.format("expected %d columns, got %d", self.columns, #fields))
  end

  local record = quoted(fields[1])
  for i = 2, self.columns do
    if not fields[i] then
      record = record .. ','
    else
      record = record .. ',' .. quoted(fields[i])
    end
  end
  return record
end

function Writer:write(fields)
  self.data = string.format("%s%s\n", self.data, self:record(fields))
end

return {Writer = Writer}
end
end

do
local _ENV = _ENV
package.preload[ "src.errors" ] = function( ... ) local arg = _G.arg;
-- For communicating errors to python.

local json = require "dkjson"
local utils = require "src.utils"

local messages = {}

local function duplicate_note_id(id, notes)
  -- Create record of duplicate-note-id error.
  assert(type(id) == "number")
  assert(#notes > 1)

  local copy = {}
  for _, note in ipairs(notes) do
    assert(type(note.title) == "string" and note.title ~= "")
    assert(type(note.filename) == "string" and note.filename ~= "")
    table.insert(copy, {id = id, title = note.title, filename = note.filename})
  end

  local message = {
    name = "duplicate-note-id",
    value = {
      id = id,
      notes = copy,
    },
  }
  table.insert(messages, message)
end

local function empty_link_target(note)
  -- Create record of empty-link-target warning.
  assert(type(note.id) == "number")
  assert(type(note.title) == "string" and note.title ~= "")
  assert(type(note.filename) == "string" and note.filename ~= "")
  local message = {
    name = "empty-link-target",
    value = {
      id = note.id,
      title = note.title,
      filename = note.filename,
    },
  }
  table.insert(messages, message)
end

local function write()
  -- Write error and warning messages to json file.
  local str = json.encode(messages)
  local ok = utils.write_text("messages.json", str)
  if ok then
    messages = {}
  end
  return ok
end

return {
  duplicate_note_id = duplicate_note_id,
  empty_link_target = empty_link_target,
  write = write,

  -- For testing purposes only.
  _messages = messages,
}
end
end

do
local _ENV = _ENV
package.preload[ "src.filters" ] = function( ... ) local arg = _G.arg;
-- Pandoc filters.

local pandoc = require "pandoc"
local errors = require "src.errors"
local links = require "src.links"
local metadata = require "src.metadata"
local utils = require "src.utils"

pandoc.utils = require "pandoc.utils"

local function preprocess()
  -- Set filename and hash attributes of level 1 Headers.
  -- The attribute values are taken from preceding metadata CodeBlocks.
  return {
    Pandoc = function(doc)
      local _metadata = {}
      for _, elem in ipairs(doc.blocks) do
        if elem.tag == "CodeBlock" then
          local ok, result = metadata.parse(elem.text)
          if ok then
            _metadata = result
          end
        elseif elem.tag == "Header" and elem.level == 1 then
          assert(_metadata.filename, "missing filename")
          assert(_metadata.hash, "missing hash")
          elem.attributes.filename = _metadata.filename
          elem.attributes.hash = _metadata.hash
        end
      end
      return doc
    end,
  }
end

local function parse_note_header(elem)
  -- Parse note header content.
  -- Returns ok, note ID and title.
  -- If it's not a proper header, ok is false and the rest of the results are nil.
  local content = elem.content

  -- Get note ID.
  local id
  if content[1].tag == "Str" then
    id = tonumber(content[1].text:match '^%d+$')
  end
  if id == nil then
    return false
  end

  -- Strip note ID and whitespace prefix.
  repeat
    table.remove(content, 1)
  until #content == 0 or content[1].tag ~= "Space"

  -- Get note title.
  local title = pandoc.utils.stringify(content)
  if not title or title == "" then
    return false
  end

  return true, id, title
end

local function init(slipbox)
  -- Split the document into sections with level 1 headers.

  local function CodeBlock(elem)
      -- Strip slipbox-metadata code block.
      if metadata.parse(elem.text) then
        return {}
      end
  end

  local function Header(elem)
    -- Save slipbox notes and set ID and title attributes in the Header.
    if elem.level ~= 1 then
      return
    end

    local ok, id, title = parse_note_header(elem)
    if not ok then
      return
    end

    local filename = elem.attributes.filename
    slipbox:save_file(filename, elem.attributes.hash)

    ok = slipbox:save_note(id, title, filename)
    if not ok then
      return
    end

    elem.identifier = id
    elem.attributes.title = title
    elem.attributes.level = elem.level  -- Gets added to parent section
    return elem
  end

  local function Pandoc(doc)
    doc.blocks = pandoc.utils.make_sections(false, nil, doc.blocks)
    return doc
  end

  return {
    Header = Header,
    CodeBlock = CodeBlock,
    Pandoc = Pandoc,
  }
end

local Collector = {}
function Collector:new(slipbox, div)
  local id = tonumber(div.identifier)
  if not id then
    return
  end

  self.__index = self
  return setmetatable({
    slipbox = slipbox,
    id = id,
    div = div,
    has_empty_link_target = false,
  }, self)
end

function Collector:Cite(elem)
  for _, citation in pairs(elem.citations) do
    self.slipbox:save_citation(self.id, "ref-" .. citation.id)
  end
end

function Collector:Image(elem)
  self.slipbox:save_image(self.id, elem.src)
end

function Collector:Link(elem)
  if not elem.target or elem.target == "" then
    self.has_empty_link_target = true
    self.slipbox:save_link {
      src = self.id,
      dest = -1,
      description = "",
      direction = "",
    }
    return
  end

  local ok, link = links.parse_note_link(elem.target)
  if ok then
    self.slipbox:save_link {
      src = self.id,
      dest = tonumber(link.target:sub(2)),
      description = elem.title,
      direction = link.direction,
    }
  end
end

function Collector:Str(elem)
  local tag = utils.hashtag_prefix(elem.text)
  if tag then
    self.slipbox:save_tag(self.id, tag)
  end
end

function Collector:filter()
  return {
    Cite = function(elem) return self:Cite(elem) end,
    Image = function (elem) return self:Image(elem) end,
    Link = function(elem) return self:Link(elem) end,
    Str = function(elem) return self:Str(elem) end,
  }
end

local function collect(slipbox)
  -- Create filter that saves citations, links and tags.
  return {
    Div = function(div)
      local col = Collector:new(slipbox, div)
      if col then
        pandoc.walk_block(div, col:filter())
        if col.has_empty_link_target then
          slipbox.invalid.has_empty_link_target[col.id] = true
        end
      end
    end
  }
end

local function hashtag()
  -- Create filter that turns #tags into links.
  return {
    Str = function(elem)
      local tag = utils.hashtag_prefix(elem.text)
      if tag then
        return {
          pandoc.Link({pandoc.Str(tag)}, '#tags/' .. tag:sub(2)),
          pandoc.Str(elem.text:sub(#tag + 1)),
        }
      end
    end
  }
end

local Modifier = {}
function Modifier:new()
  self.__index = self
  return setmetatable({
    footnotes = {},
  }, self)
end

function Modifier.Image(elem)
  -- Lazy load images.
  elem.attributes.loading = "lazy"
  return elem
end

function Modifier.Link(elem)
  -- Rewrite links with empty targets/text, and remove direction prefix from
  -- URL targets.
  if not elem.target or elem.target == "" then
    return elem.content
  end

  local ok, link = links.parse_note_link(elem.target)
  if ok then
    elem.target = link.target
  end

  local content = pandoc.utils.stringify(elem.content or "")

  if content ~= "" then return elem end
  return {
    pandoc.Str " [",
    pandoc.Link(
      {pandoc.Str(elem.target)},
      elem.target,
      elem.title),
    pandoc.Str "]",
  }
end

function Modifier:Note(elem)
  -- Collect footnotes.
  table.insert(self.footnotes, pandoc.Div(elem.content))
  local count = #self.footnotes
  return pandoc.Superscript(pandoc.Str(tostring(count)))
end

function Modifier:filter()
  return {
    Image = function(elem) return self.Image(elem) end,
    Link = function(elem) return self.Link(elem) end,
    Note = function(elem) return self:Note(elem) end,
  }
end

local function modify()
  -- Create filter that modifies the document.
  return {
    Div = function(div)
      local mod = Modifier:new()
      div = pandoc.walk_block(div, mod:filter())
      if next(mod.footnotes) then
        local ol = pandoc.OrderedList{}
        for _, block in ipairs(mod.footnotes) do
          table.insert(ol.content, {block})
        end
        table.insert(div.content, pandoc.HorizontalRule())
        table.insert(div.content, ol)
      end

      if div.attributes.level then
        if div.attributes.level == "1" then
          table.insert(div.classes, "slipbox-note")
        end
        div.attributes.level = nil
      end
      return div
    end
  }
end

local function to_html(block)
  local doc = pandoc.Pandoc{block}
  return pandoc.write(doc, "html")
end

local function citations(slipbox)
  return {
    Div = function(div)
      -- Suppress bibliography.
      if div.identifier == "refs" then

        local function Div(elem)
          -- Save reference HTML entry.
          local identifier = elem.identifier
          if utils.is_reference_id(identifier) then
            elem.identifier = ""
            slipbox:save_reference(identifier, to_html(elem))
          end
        end

        pandoc.walk_block(div, {Div = Div})
        return {}
      end
    end,
  }
end

local function serialize(slipbox)
  -- Create filter to dump slipbox data into working directory.
  return {
    Pandoc = function()
      slipbox:write_data()
    end
  }
end

local function check(slipbox)
  -- Check for empty link targets.
  return {
    Pandoc = function()
      local has_empty_link_target = {}
      for id in pairs(slipbox.invalid.has_empty_link_target) do
        table.insert(has_empty_link_target, id)
      end
      if #has_empty_link_target == 0 then
        return
      end

      table.sort(has_empty_link_target)

      for _, id in ipairs(has_empty_link_target) do
        local note = slipbox.notes[id] or {}
        local title = note.title
        local filename = note.filename
        if title and filename then
          errors.empty_link_target{id = id, title = title, filename = filename}
        end
      end
    end
  }
end

local function cleanup()
  return {
    Header = function(elem)
      elem.attributes = {}
      return elem
    end,
    Div = function(elem)
      elem.attributes.hash = nil
      return elem
    end,
    Pandoc = function()
      -- Output all recorded errors.
      errors.write()
    end,
  }
end

return {
  preprocess = preprocess,
  init = init,
  collect = collect,
  hashtag = hashtag,
  modify = modify,
  citations = citations,
  serialize = serialize,
  check = check,
  cleanup = cleanup,
}
end
end

do
local _ENV = _ENV
package.preload[ "src.links" ] = function( ... ) local arg = _G.arg;
local translation = {
  [""] = "",
  ["<"] = "<",
  [">"] = ">",
  ["%3e"] = ">",
  ["%3E"] = ">",
  ["%3c"] = "<",
  ["%3C"] = "<",
}
local function normalize_direction(direction)
  return translation[direction]
end

local function parse_note_link(target)
  -- Return ok and parsed result.
  local pattern = "^(.*)(#%d+)$"
  local prefix, target_ = string.match(target, pattern)

  if target_ == nil then
    return false
  end

  local direction = normalize_direction(prefix)
  if direction == nil then
    return false
  end
  return true, {
    direction = normalize_direction(prefix),
    target = target_,
  }
end

return {
  parse_note_link = parse_note_link,
}
end
end

do
local _ENV = _ENV
package.preload[ "src.metadata" ] = function( ... ) local arg = _G.arg;
-- Metadata parser.

local function strip(text)
  -- Strip leading and trailing whitespace.
  return text:match('^%s*(.-)%s*$')
end

local function strip_header(text)
  local pattern = '^%[slipbox%-metadata%]\n(.-)$'
  return text:match(pattern)
end

local function lines(text)
  local str = text
  return function()
    if str ~= "" then
      local index = str:find '\n' or #str
      local result = str:sub(1, index)
      str = str:sub(index + 1)
      return result
    end
  end
end

local function parse_line(line)
  local key = line:match '^(.-)='
  local val = line:match '^.-=(.*)$'
  if key and val then
    return strip(key), strip(val)
  end
end

local function parse(text)
  -- Return ok, parsed metadata.
  local body = strip_header(text)
  if not body then
    return false
  end

  local metadata = {}
  for line in lines(strip(body)) do
    local key, val = parse_line(line)
    if not (key and val) then
      return false
    end
    metadata[key] = val
  end
  return true, metadata
end

return {parse = parse}
end
end

do
local _ENV = _ENV
package.preload[ "src.slipbox" ] = function( ... ) local arg = _G.arg;
local csv = require "src.csv"
local errors = require "src.errors"
local utils = require "src.utils"

local SlipBox = {}
function SlipBox:new()
  self.__index = self
  return setmetatable({
    files = {},
    notes = {},
    tags = {},
    links = {},
    citations = {},
    images = {},
    bibliography = {},
    invalid = {
      has_empty_link_target = {},
    },
  }, self)
end

function SlipBox:save_file(filename, hash)
  assert(type(filename) == "string")
  assert(type(hash) == "string")
  assert(self.files[filename] == nil or self.files[filename] == hash)
  self.files[filename] = hash
end

function SlipBox:save_citation(id, citation)
  -- Save citation from note id (number).
  assert(type(id) == "number")
  local citations = self.citations[id] or {}
  citations[citation] = true
  self.citations[id] = citations
end

function SlipBox:save_image(id, filename)
  assert(type(id) == "number")
  assert(type(filename) == "string")

  local image = self.images[filename] or {
    id = id,
    filename = filename,
    notes = {},
  }
  self.images[filename] = image
  image.notes[id] = true
end

function SlipBox:save_reference(id, html)
  -- Save reference into slipbox.
  assert(type(id) == "string")
  assert(type(html) == "string")
  assert(id ~= "")
  assert(html ~= "")
  self.bibliography[id] = html
end

function SlipBox:save_note(id, title, filename)
  -- Save note into slipbox.
  -- Returns false if a note with the same ID already exists, true otherwise.
  -- Logs errors if any.
  assert(type(id) == "number")
  assert(type(title) == "string")
  assert(type(filename) == "string")
  assert(title ~= "")
  assert(filename ~= "")

  local note = self.notes[id]
  if note and (note.title ~= title or note.filename ~= filename) then
    errors.duplicate_note_id(id, {note, {title = title, filename = filename}})
    return false
  end
  self.notes[id] = {title = title, filename = filename}
  return true
end

function SlipBox:save_tag(id, tag)
  assert(type(id) == "number")
  assert(type(tag) == "string")
  assert(tag ~= "")

  local tags = self.tags[id] or {}
  tags[tag] = true
  self.tags[id] = tags
end

function SlipBox:save_link(link)
  if link and link.src then
    local links = self.links[link.src] or {}
    table.insert(links, link)
    self.links[link.src] = links
  end
end

local function notes_to_csv(notes)
  -- Generate CSV data from slipbox notes.
  local w = csv.Writer:new{"id", "title", "filename"}
  for id, note in pairs(notes) do
    if note.filename then
      w:write{id, note.title, note.filename}
    end
  end
  return w.data
end

local function tags_to_csv(all_tags)
  -- Create CSV data from tags in slipbox.
  local w = csv.Writer:new{"tag", "id"}
  for id, tags in pairs(all_tags) do
    for tag, _ in pairs(tags) do
      w:write{tag, id}
    end
  end
  return w.data
end

local function links_to_csv(links)
  -- Create CSV data from direct links in slipbox.
  local w = csv.Writer:new{"src", "dest", "direction"}
  for src, dests in pairs(links) do
    for _, dest in ipairs(dests) do
      w:write{src, dest.dest, dest.direction}
    end
  end
  return w.data
end

local function bibliography_to_csv(refs)
  local w = csv.Writer:new{"key", "html"}
  for ref, html in pairs(refs) do
    w:write{ref, html}
  end
  return w.data
end

local function files_to_csv(files)
  local w = csv.Writer:new{"filename", "hash"}
  for filename, hash in pairs(files) do
    w:write{filename, hash}
  end
  return w.data
end

local function citations_to_csv(citations)
  local w = csv.Writer:new{"note", "reference"}
  for id, cites in pairs(citations) do
    for cite in pairs(cites) do
      w:write{id, cite}
    end
  end
  return w.data
end

local function images_to_csv(images)
  local w = csv.Writer:new{"filename"}
  for filename in pairs(images) do
    w:write{filename}
  end
  return w.data
end

local function image_links_to_csv(images)
  local w = csv.Writer:new{"note", "image"}
  for filename, image in pairs(images) do
    for note in pairs(image.notes) do
      w:write{note, filename}
    end
  end
  return w.data
end

function SlipBox:write_data()
  -- Create CSV data to files.
  local write = utils.write_text
  write("files.csv", files_to_csv(self.files))
  write("notes.csv", notes_to_csv(self.notes))
  write("tags.csv", tags_to_csv(self.tags))
  write("links.csv", links_to_csv(self.links))
  write("images.csv", images_to_csv(self.images))
  write("image_links.csv", image_links_to_csv(self.images))
  write("bibliography.csv", bibliography_to_csv(self.bibliography))
  write("citations.csv", citations_to_csv(self.citations))
end

return {
  SlipBox = SlipBox,
}
end
end

do
local _ENV = _ENV
package.preload[ "src.utils" ] = function( ... ) local arg = _G.arg;
local function hashtag_prefix(s)
  return s:match '^#[-_a-zA-Z0-9]+'
end

local function append_text(filename, text)
  local file = io.open(filename, 'a')
  if not file then
    return false
  end
  file:write(text)
  file:close()
  return true
end

local function write_text(filename, text)
  local file = io.open(filename, 'w')
  if not file then
    return false
  end
  file:write(text)
  file:close()
  return true
end

local function is_reference_id(text)
  -- Check if text (string) is a reference identifier.
  return text:match('^ref%-.+$') and true or false
end

return {
  is_reference_id = is_reference_id,
  hashtag_prefix = hashtag_prefix,
  write_text = write_text,
  append_text = append_text,
}
end
end

local filters = require "src.filters"
local slipbox = require "src.slipbox"

local current_slipbox = slipbox.SlipBox:new()

return {
  filters.preprocess(),
  filters.init(current_slipbox),
  filters.collect(current_slipbox),
  filters.hashtag(),
  filters.modify(current_slipbox),
  filters.citations(current_slipbox),
  filters.serialize(current_slipbox),
  filters.check(current_slipbox),
  filters.cleanup(),
}
