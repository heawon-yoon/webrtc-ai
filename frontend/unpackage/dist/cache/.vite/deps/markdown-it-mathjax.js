import {
  __commonJS
} from "./chunk-ZS7NZCD4.js";

// ../../../../../../Users/yoon/Desktop/heawon’s MacBook Pro/aiprojs/webrtc-ai/frontend/node_modules/markdown-it-mathjax/markdown-it-mathjax.js
var require_markdown_it_mathjax = __commonJS({
  "../../../../../../Users/yoon/Desktop/heawon’s MacBook Pro/aiprojs/webrtc-ai/frontend/node_modules/markdown-it-mathjax/markdown-it-mathjax.js"(exports, module) {
    (function(root, factory) {
      if (typeof exports === "object") {
        module.exports = factory();
      } else {
        root.markdownitMathjax = factory();
      }
    })(exports, function() {
      function math(state, silent) {
        var startMathPos = state.pos;
        if (state.src.charCodeAt(startMathPos) !== 92) {
          return false;
        }
        var match = state.src.slice(++startMathPos).match(/^(?:\\\[|\\\(|begin\{([^}]*)\})/);
        if (!match) {
          return false;
        }
        startMathPos += match[0].length;
        var type, endMarker, includeMarkers;
        if (match[0] === "\\[") {
          type = "display_math";
          endMarker = "\\\\]";
        } else if (match[0] === "\\(") {
          type = "inline_math";
          endMarker = "\\\\)";
        } else if (match[1]) {
          type = "math";
          endMarker = "\\end{" + match[1] + "}";
          includeMarkers = true;
        }
        var endMarkerPos = state.src.indexOf(endMarker, startMathPos);
        if (endMarkerPos === -1) {
          return false;
        }
        var nextPos = endMarkerPos + endMarker.length;
        if (!silent) {
          var token = state.push(type, "", 0);
          token.content = includeMarkers ? state.src.slice(state.pos, nextPos) : state.src.slice(startMathPos, endMarkerPos);
        }
        state.pos = nextPos;
        return true;
      }
      function texMath(state, silent) {
        var startMathPos = state.pos;
        if (state.src.charCodeAt(startMathPos) !== 36) {
          return false;
        }
        var endMarker = "$";
        var afterStartMarker = state.src.charCodeAt(++startMathPos);
        if (afterStartMarker === 36) {
          endMarker = "$$";
          if (state.src.charCodeAt(++startMathPos) === 36) {
            return false;
          }
        } else {
          if (afterStartMarker === 32 || afterStartMarker === 9 || afterStartMarker === 10) {
            return false;
          }
        }
        var endMarkerPos = state.src.indexOf(endMarker, startMathPos);
        if (endMarkerPos === -1) {
          return false;
        }
        if (state.src.charCodeAt(endMarkerPos - 1) === 92) {
          return false;
        }
        var nextPos = endMarkerPos + endMarker.length;
        if (endMarker.length === 1) {
          var beforeEndMarker = state.src.charCodeAt(endMarkerPos - 1);
          if (beforeEndMarker === 32 || beforeEndMarker === 9 || beforeEndMarker === 10) {
            return false;
          }
          var suffix = state.src.charCodeAt(nextPos);
          if (suffix >= 48 && suffix < 58) {
            return false;
          }
        }
        if (!silent) {
          var token = state.push(endMarker.length === 1 ? "inline_math" : "display_math", "", 0);
          token.content = state.src.slice(startMathPos, endMarkerPos);
        }
        state.pos = nextPos;
        return true;
      }
      function escapeHtml(html) {
        return html.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/\u00a0/g, " ");
      }
      function extend(options, defaults) {
        return Object.keys(defaults).reduce(function(result, key) {
          if (result[key] === void 0) {
            result[key] = defaults[key];
          }
          return result;
        }, options);
      }
      var mapping = {
        "math": "Math",
        "inline_math": "InlineMath",
        "display_math": "DisplayMath"
      };
      return function(options) {
        var defaults = {
          beforeMath: "",
          afterMath: "",
          beforeInlineMath: "\\(",
          afterInlineMath: "\\)",
          beforeDisplayMath: "\\[",
          afterDisplayMath: "\\]"
        };
        options = extend(options || {}, defaults);
        return function(md) {
          md.inline.ruler.before("escape", "math", math);
          md.inline.ruler.push("texMath", texMath);
          Object.keys(mapping).forEach(function(key) {
            var before = options["before" + mapping[key]];
            var after = options["after" + mapping[key]];
            md.renderer.rules[key] = function(tokens, idx) {
              return before + escapeHtml(tokens[idx].content) + after;
            };
          });
        };
      };
    });
  }
});
export default require_markdown_it_mathjax();
//# sourceMappingURL=markdown-it-mathjax.js.map
