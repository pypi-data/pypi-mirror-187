(()=>{"use strict";var e,t={3409:(e,t,r)=>{var i=r(211);class o extends i.I{constructor(){super(...arguments),this.chooserModalClass=ImageChooserModal}initHTMLElements(e){super.initHTMLElements(e),this.previewImage=this.chooserElement.querySelector("[data-chooser-image]")}getStateFromHTML(){const e=super.getStateFromHTML();return e&&(e.preview={url:this.previewImage.getAttribute("src"),width:this.previewImage.getAttribute("width"),height:this.previewImage.getAttribute("height")}),e}renderState(e){super.renderState(e),this.previewImage.setAttribute("src",e.preview.url),this.previewImage.setAttribute("width",e.preview.width)}}class s extends i.G{constructor(){super(...arguments),this.widgetClass=o,this.chooserModalClass=ImageChooserModal}}window.telepath.register("wagtail.images.widgets.ImageChooser",s)},5311:e=>{e.exports=jQuery}},r={};function i(e){var o=r[e];if(void 0!==o)return o.exports;var s=r[e]={exports:{}};return t[e](s,s.exports,i),s.exports}i.m=t,e=[],i.O=(t,r,o,s)=>{if(!r){var a=1/0;for(h=0;h<e.length;h++){for(var[r,o,s]=e[h],n=!0,l=0;l<r.length;l++)(!1&s||a>=s)&&Object.keys(i.O).every((e=>i.O[e](r[l])))?r.splice(l--,1):(n=!1,s<a&&(a=s));if(n){e.splice(h--,1);var u=o();void 0!==u&&(t=u)}}return t}s=s||0;for(var h=e.length;h>0&&e[h-1][2]>s;h--)e[h]=e[h-1];e[h]=[r,o,s]},i.n=e=>{var t=e&&e.__esModule?()=>e.default:()=>e;return i.d(t,{a:t}),t},i.d=(e,t)=>{for(var r in t)i.o(t,r)&&!i.o(e,r)&&Object.defineProperty(e,r,{enumerable:!0,get:t[r]})},i.g=function(){if("object"==typeof globalThis)return globalThis;try{return this||new Function("return this")()}catch(e){if("object"==typeof window)return window}}(),i.o=(e,t)=>Object.prototype.hasOwnProperty.call(e,t),i.r=e=>{"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},i.j=810,(()=>{var e={810:0};i.O.j=t=>0===e[t];var t=(t,r)=>{var o,s,[a,n,l]=r,u=0;if(a.some((t=>0!==e[t]))){for(o in n)i.o(n,o)&&(i.m[o]=n[o]);if(l)var h=l(i)}for(t&&t(r);u<a.length;u++)s=a[u],i.o(e,s)&&e[s]&&e[s][0](),e[s]=0;return i.O(h)},r=globalThis.webpackChunkwagtail=globalThis.webpackChunkwagtail||[];r.forEach(t.bind(null,0)),r.push=t.bind(null,r.push.bind(r))})();var o=i.O(void 0,[751],(()=>i(3409)));o=i.O(o)})();