(()=>{"use strict";var e,a={2618:(e,a,t)=>{var n=t(5311),i=t.n(n),l=t(1544);function d(e,a){const t=e+"-handsontable-container",n=e+"-handsontable-header",d=e+"-handsontable-col-header",r=e+"-handsontable-col-caption",o=i()("#"+e),s=i()("#"+n),c=i()("#"+d),h=i()("#"+r),f={};let p=null,u=null,b=!1;const w=function(){const a=i()("#"+e).parent();return a.find(".htCore").height()+2*a.find("[data-field]").height()},v=["[data-field] > .handsontable",".wtHider",".wtHolder"],_=function(a){const t=i()("#"+e);i().each(v,(function(){t.closest("[data-field]").find(this).height(a)}))};try{u=JSON.parse(o.val())}catch(e){}null!==u&&((0,l.R)(u,"first_row_is_table_header")&&s.prop("checked",u.first_row_is_table_header),(0,l.R)(u,"first_col_is_header")&&c.prop("checked",u.first_col_is_header),(0,l.R)(u,"table_caption")&&h.prop("value",u.table_caption)),((0,l.R)(!a,"width")||(0,l.R)(!a,"height"))&&i()(window).on("resize",(()=>{var e;p.updateSettings({width:i()(".w-field--table_input").closest(".sequence-member-inner").width(),height:w()}),e="100%",i().each(v,(function(){i()(this).width(e)})),i()(".w-field--table_input").width(e)}));const g=function(){const e=p.getCellsMeta(),a=[];for(let t=0;t<e.length;t+=1)(0,l.R)(e[t],"className")&&a.push({row:e[t].row,col:e[t].col,className:e[t].className});return a},m=function(){o.val(JSON.stringify({data:p.getData(),cell:g(),first_row_is_table_header:s.prop("checked"),first_col_is_header:c.prop("checked"),table_caption:h.val()}))},y=function(e,a){_(w()),m()};s.on("change",(()=>{m()})),c.on("change",(()=>{m()})),h.on("change",(()=>{m()}));const $={afterChange:function(e,a){"loadData"!==a&&m()},afterCreateCol:y,afterCreateRow:y,afterRemoveCol:y,afterRemoveRow:y,afterSetCellMeta:function(e,a,t,n){b&&"className"===t&&m()},afterInit:function(){b=!0}};null!==u&&((0,l.R)(u,"data")&&($.data=u.data),(0,l.R)(u,"cell")&&($.cell=u.cell)),Object.keys($).forEach((e=>{f[e]=$[e]})),Object.keys(a).forEach((e=>{f[e]=a[e]})),p=new Handsontable(document.getElementById(t),f),p.render(),"resize"in i()(window)&&(_(w()),i()(window).on("load",(()=>{i()(window).trigger("resize")})))}window.initTable=d,window.telepath.register("wagtail.widgets.TableInput",class{constructor(e,a){this.options=e,this.strings=a}render(e,a,t,n){const i=document.createElement("div");i.innerHTML=`\n      <div className="w-field__wrapper" data-field-wrapper>\n        <label class="w-field__label" for="${t}-handsontable-header">${this.strings["Row header"]}</label>\n        <div class="w-field w-field--boolean_field w-field--checkbox_input" data-field>\n          <div className="w-field__input" data-field-input>\n            <input type="checkbox" id="${t}-handsontable-header" name="handsontable-header" aria-describedby="${t}-handsontable-header-helptext" />\n          </div>\n          <div id="${t}-handsontable-header-helptext" data-field-help>\n            <div class="help">${this.strings["Display the first row as a header."]}</div>\n          </div>\n        </div>\n      </div>\n      <div className="w-field__wrapper" data-field-wrapper>\n        <label class="w-field__label" for="${t}-handsontable-col-header">${this.strings["Column header"]}</label>\n        <div class="w-field w-field--boolean_field w-field--checkbox_input" data-field>\n          <div className="w-field__input" data-field-input>\n            <input type="checkbox" id="${t}-handsontable-col-header" name="handsontable-col-header" aria-describedby="${t}-handsontable-col-header-helptext" />\n          </div>\n          <div id="${t}-handsontable-col-header-helptext" data-field-help>\n            <div class="help">${this.strings["Display the first column as a header."]}</div>\n          </div>\n        </div>\n      </div>\n      <div className="w-field__wrapper" data-field-wrapper>\n        <label class="w-field__label" for="${t}-handsontable-col-caption">${this.strings["Table caption"]}</label>\n        <div class="w-field w-field--char_field w-field--text_input" data-field>\n          <div className="w-field__input" data-field-input>\n            <input type="text" id="${t}-handsontable-col-caption" name="handsontable-col-caption" aria-describedby="${t}-handsontable-col-caption-helptext" />\n          </div>\n          <div id="${t}-handsontable-col-caption-helptext" data-field-help>\n            <div class="help">${this.strings["A heading that identifies the overall topic of the table, and is useful for screen reader users"]}</div>\n          </div>\n        </div>\n      </div>\n      <div id="${t}-handsontable-container"></div>\n      <input type="hidden" name="${a}" id="${t}" placeholder="${this.strings.Table}">\n    `,e.replaceWith(i);const l=i.querySelector(`input[name="${a}"]`),r=this.options,o={getValue:()=>JSON.parse(l.value),getState:()=>JSON.parse(l.value),setState(e){l.value=JSON.stringify(e),d(t,r)},focus(){}};return o.setState(n),o}})},5311:e=>{e.exports=jQuery}},t={};function n(e){var i=t[e];if(void 0!==i)return i.exports;var l=t[e]={exports:{}};return a[e](l,l.exports,n),l.exports}n.m=a,e=[],n.O=(a,t,i,l)=>{if(!t){var d=1/0;for(c=0;c<e.length;c++){for(var[t,i,l]=e[c],r=!0,o=0;o<t.length;o++)(!1&l||d>=l)&&Object.keys(n.O).every((e=>n.O[e](t[o])))?t.splice(o--,1):(r=!1,l<d&&(d=l));if(r){e.splice(c--,1);var s=i();void 0!==s&&(a=s)}}return a}l=l||0;for(var c=e.length;c>0&&e[c-1][2]>l;c--)e[c]=e[c-1];e[c]=[t,i,l]},n.n=e=>{var a=e&&e.__esModule?()=>e.default:()=>e;return n.d(a,{a}),a},n.d=(e,a)=>{for(var t in a)n.o(a,t)&&!n.o(e,t)&&Object.defineProperty(e,t,{enumerable:!0,get:a[t]})},n.g=function(){if("object"==typeof globalThis)return globalThis;try{return this||new Function("return this")()}catch(e){if("object"==typeof window)return window}}(),n.o=(e,a)=>Object.prototype.hasOwnProperty.call(e,a),n.r=e=>{"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},n.j=986,(()=>{var e={986:0};n.O.j=a=>0===e[a];var a=(a,t)=>{var i,l,[d,r,o]=t,s=0;if(d.some((a=>0!==e[a]))){for(i in r)n.o(r,i)&&(n.m[i]=r[i]);if(o)var c=o(n)}for(a&&a(t);s<d.length;s++)l=d[s],n.o(e,l)&&e[l]&&e[l][0](),e[l]=0;return n.O(c)},t=globalThis.webpackChunkwagtail=globalThis.webpackChunkwagtail||[];t.forEach(a.bind(null,0)),t.push=a.bind(null,t.push.bind(t))})();var i=n.O(void 0,[751],(()=>n(2618)));i=n.O(i)})();