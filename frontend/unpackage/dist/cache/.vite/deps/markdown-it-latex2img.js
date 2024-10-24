import {
  __commonJS
} from "./chunk-ZS7NZCD4.js";

// ../../../../../../Users/yoon/Desktop/heawon’s MacBook Pro/aiprojs/webrtc-ai/frontend/node_modules/markdown-it-latex2img/index.js
var require_markdown_it_latex2img = __commonJS({
  "../../../../../../Users/yoon/Desktop/heawon’s MacBook Pro/aiprojs/webrtc-ai/frontend/node_modules/markdown-it-latex2img/index.js"(exports, module) {
    function isValidDelim(state, pos) {
      let prevChar, nextChar, max = state.posMax, can_open = true, can_close = true;
      prevChar = pos > 0 ? state.src.charCodeAt(pos - 1) : -1;
      nextChar = pos + 1 <= max ? state.src.charCodeAt(pos + 1) : -1;
      if (prevChar === 32 || prevChar === 9 || nextChar >= 48 && nextChar <= 57) {
        can_close = false;
      }
      if (nextChar === 32 || nextChar === 9) {
        can_open = false;
      }
      return {
        can_open,
        can_close
      };
    }
    function math_inline(state, silent) {
      let start, match, token, res, pos;
      if (state.src[state.pos] !== "$") {
        return false;
      }
      res = isValidDelim(state, state.pos);
      if (!res.can_open) {
        if (!silent) {
          state.pending += "$";
        }
        state.pos += 1;
        return true;
      }
      start = state.pos + 1;
      match = start;
      while ((match = state.src.indexOf("$", match)) !== -1) {
        pos = match - 1;
        while (state.src[pos] === "\\") {
          pos -= 1;
        }
        if ((match - pos) % 2 == 1) {
          break;
        }
        match += 1;
      }
      if (match === -1) {
        if (!silent) {
          state.pending += "$";
        }
        state.pos = start;
        return true;
      }
      if (match - start === 0) {
        if (!silent) {
          state.pending += "$$";
        }
        state.pos = start + 1;
        return true;
      }
      res = isValidDelim(state, match);
      if (!res.can_close) {
        if (!silent) {
          state.pending += "$";
        }
        state.pos = start;
        return true;
      }
      if (!silent) {
        token = state.push("math_inline", "math", 0);
        token.markup = "$";
        token.content = state.src.slice(start, match);
      }
      state.pos = match + 1;
      return true;
    }
    function math_block(state, start, end, silent) {
      let firstLine, lastLine, next, lastPos, found = false, token, pos = state.bMarks[start] + state.tShift[start], max = state.eMarks[start];
      if (pos + 2 > max) {
        return false;
      }
      if (state.src.slice(pos, pos + 2) !== "$$") {
        return false;
      }
      pos += 2;
      firstLine = state.src.slice(pos, max);
      if (silent) {
        return true;
      }
      if (firstLine.trim().slice(-2) === "$$") {
        firstLine = firstLine.trim().slice(0, -2);
        found = true;
      }
      for (next = start; !found; ) {
        next++;
        if (next >= end) {
          break;
        }
        pos = state.bMarks[next] + state.tShift[next];
        max = state.eMarks[next];
        if (pos < max && state.tShift[next] < state.blkIndent) {
          break;
        }
        if (state.src.slice(pos, max).trim().slice(-2) === "$$") {
          lastPos = state.src.slice(0, max).lastIndexOf("$$");
          lastLine = state.src.slice(pos, lastPos);
          found = true;
        }
      }
      state.line = next + 1;
      token = state.push("math_block", "math", 0);
      token.block = true;
      token.content = (firstLine && firstLine.trim() ? firstLine + "\n" : "") + state.getLines(start + 1, next, state.tShift[start], true) + (lastLine && lastLine.trim() ? lastLine : "");
      token.map = [start, state.line];
      token.markup = "$$";
      return true;
    }
    module.exports = (md, options) => {
      options = options || {};
      options.server = options.server || "https://math.now.sh";
      options.style = options.style || "";
      const purifiedURL = (latex) => {
        return encodeURIComponent(latex).replace("(", "%28").replace(")", "%29");
      };
      let Inline = (latex) => {
        try {
          return `<img src="${options.server}?inline=${purifiedURL(latex)}" style="${options.style}display:inline-block;margin: 0;"/>`;
        } catch (error) {
          console.error(error);
          return latex;
        }
      };
      let Block = (latex) => {
        try {
          return `<p style="${options.style}"><img src="${options.server}?from=${purifiedURL(
            latex
          )}" /></p>`;
        } catch (error) {
          console.error(error);
          return latex;
        }
      };
      md.inline.ruler.after("escape", "math_inline", math_inline);
      md.block.ruler.after("blockquote", "math_block", math_block, {
        alt: ["paragraph", "reference", "blockquote", "list"]
      });
      md.renderer.rules.math_inline = (tokens, idx) => {
        return Inline(tokens[idx].content);
      };
      md.renderer.rules.math_block = (tokens, idx) => {
        return Block(tokens[idx].content);
      };
    };
  }
});
export default require_markdown_it_latex2img();
//# sourceMappingURL=markdown-it-latex2img.js.map
