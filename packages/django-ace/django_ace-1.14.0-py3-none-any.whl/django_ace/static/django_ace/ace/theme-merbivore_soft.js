define("ace/theme/merbivore_soft.css",["require","exports","module"], function(require, exports, module){module.exports = ".ace-merbivore-soft .ace_gutter {\n  background: #262424;\n  color: #E6E1DC\n}\n\n.ace-merbivore-soft .ace_print-margin {\n  width: 1px;\n  background: #262424\n}\n\n.ace-merbivore-soft {\n  background-color: #1C1C1C;\n  color: #E6E1DC\n}\n\n.ace-merbivore-soft .ace_cursor {\n  color: #FFFFFF\n}\n\n.ace-merbivore-soft .ace_marker-layer .ace_selection {\n  background: #494949\n}\n\n.ace-merbivore-soft.ace_multiselect .ace_selection.ace_start {\n  box-shadow: 0 0 3px 0px #1C1C1C;\n}\n\n.ace-merbivore-soft .ace_marker-layer .ace_step {\n  background: rgb(102, 82, 0)\n}\n\n.ace-merbivore-soft .ace_marker-layer .ace_bracket {\n  margin: -1px 0 0 -1px;\n  border: 1px solid #404040\n}\n\n.ace-merbivore-soft .ace_marker-layer .ace_active-line {\n  background: #333435\n}\n\n.ace-merbivore-soft .ace_gutter-active-line {\n  background-color: #333435\n}\n\n.ace-merbivore-soft .ace_marker-layer .ace_selected-word {\n  border: 1px solid #494949\n}\n\n.ace-merbivore-soft .ace_invisible {\n  color: #404040\n}\n\n.ace-merbivore-soft .ace_entity.ace_name.ace_tag,\n.ace-merbivore-soft .ace_keyword,\n.ace-merbivore-soft .ace_meta,\n.ace-merbivore-soft .ace_meta.ace_tag,\n.ace-merbivore-soft .ace_storage {\n  color: #FC803A\n}\n\n.ace-merbivore-soft .ace_constant,\n.ace-merbivore-soft .ace_constant.ace_character,\n.ace-merbivore-soft .ace_constant.ace_character.ace_escape,\n.ace-merbivore-soft .ace_constant.ace_other,\n.ace-merbivore-soft .ace_support.ace_type {\n  color: #68C1D8\n}\n\n.ace-merbivore-soft .ace_constant.ace_character.ace_escape {\n  color: #B3E5B4\n}\n\n.ace-merbivore-soft .ace_constant.ace_language {\n  color: #E1C582\n}\n\n.ace-merbivore-soft .ace_constant.ace_library,\n.ace-merbivore-soft .ace_string,\n.ace-merbivore-soft .ace_support.ace_constant {\n  color: #8EC65F\n}\n\n.ace-merbivore-soft .ace_constant.ace_numeric {\n  color: #7FC578\n}\n\n.ace-merbivore-soft .ace_invalid,\n.ace-merbivore-soft .ace_invalid.ace_deprecated {\n  color: #FFFFFF;\n  background-color: #FE3838\n}\n\n.ace-merbivore-soft .ace_fold {\n  background-color: #FC803A;\n  border-color: #E6E1DC\n}\n\n.ace-merbivore-soft .ace_comment,\n.ace-merbivore-soft .ace_meta {\n  font-style: italic;\n  color: #AC4BB8\n}\n\n.ace-merbivore-soft .ace_entity.ace_other.ace_attribute-name {\n  color: #EAF1A3\n}\n\n.ace-merbivore-soft .ace_indent-guide {\n  background: url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAACCAYAAACZgbYnAAAAEklEQVQImWOQkpLyZfD09PwPAAfYAnaStpHRAAAAAElFTkSuQmCC) right repeat-y\n}\n\n.ace-merbivore-soft .ace_indent-guide-active {\n  background: url(\"data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAACCAYAAACZgbYnAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAIGNIUk0AAHolAACAgwAA+f8AAIDpAAB1MAAA6mAAADqYAAAXb5JfxUYAAAAZSURBVHjaYvj///9/hivKyv8BAAAA//8DACLqBhbvk+/eAAAAAElFTkSuQmCC\") right repeat-y;\n}\n";

});

define("ace/theme/merbivore_soft",["require","exports","module","ace/theme/merbivore_soft.css","ace/lib/dom"], function(require, exports, module){exports.isDark = true;
exports.cssClass = "ace-merbivore-soft";
exports.cssText = require("./merbivore_soft.css");
var dom = require("../lib/dom");
dom.importCssString(exports.cssText, exports.cssClass, false);

});                (function() {
                    window.require(["ace/theme/merbivore_soft"], function(m) {
                        if (typeof module == "object" && typeof exports == "object" && module) {
                            module.exports = m;
                        }
                    });
                })();
            