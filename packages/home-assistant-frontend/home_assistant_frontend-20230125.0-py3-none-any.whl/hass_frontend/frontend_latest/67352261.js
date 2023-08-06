/*! For license information please see 67352261.js.LICENSE.txt */
"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[80938],{21157:(e,t,l)=>{l(48175);const n=l(50856).d`
/* Most common used flex styles*/
<dom-module id="iron-flex">
  <template>
    <style>
      .layout.horizontal,
      .layout.vertical {
        display: -ms-flexbox;
        display: -webkit-flex;
        display: flex;
      }

      .layout.inline {
        display: -ms-inline-flexbox;
        display: -webkit-inline-flex;
        display: inline-flex;
      }

      .layout.horizontal {
        -ms-flex-direction: row;
        -webkit-flex-direction: row;
        flex-direction: row;
      }

      .layout.vertical {
        -ms-flex-direction: column;
        -webkit-flex-direction: column;
        flex-direction: column;
      }

      .layout.wrap {
        -ms-flex-wrap: wrap;
        -webkit-flex-wrap: wrap;
        flex-wrap: wrap;
      }

      .layout.no-wrap {
        -ms-flex-wrap: nowrap;
        -webkit-flex-wrap: nowrap;
        flex-wrap: nowrap;
      }

      .layout.center,
      .layout.center-center {
        -ms-flex-align: center;
        -webkit-align-items: center;
        align-items: center;
      }

      .layout.center-justified,
      .layout.center-center {
        -ms-flex-pack: center;
        -webkit-justify-content: center;
        justify-content: center;
      }

      .flex {
        -ms-flex: 1 1 0.000000001px;
        -webkit-flex: 1;
        flex: 1;
        -webkit-flex-basis: 0.000000001px;
        flex-basis: 0.000000001px;
      }

      .flex-auto {
        -ms-flex: 1 1 auto;
        -webkit-flex: 1 1 auto;
        flex: 1 1 auto;
      }

      .flex-none {
        -ms-flex: none;
        -webkit-flex: none;
        flex: none;
      }
    </style>
  </template>
</dom-module>
/* Basic flexbox reverse styles */
<dom-module id="iron-flex-reverse">
  <template>
    <style>
      .layout.horizontal-reverse,
      .layout.vertical-reverse {
        display: -ms-flexbox;
        display: -webkit-flex;
        display: flex;
      }

      .layout.horizontal-reverse {
        -ms-flex-direction: row-reverse;
        -webkit-flex-direction: row-reverse;
        flex-direction: row-reverse;
      }

      .layout.vertical-reverse {
        -ms-flex-direction: column-reverse;
        -webkit-flex-direction: column-reverse;
        flex-direction: column-reverse;
      }

      .layout.wrap-reverse {
        -ms-flex-wrap: wrap-reverse;
        -webkit-flex-wrap: wrap-reverse;
        flex-wrap: wrap-reverse;
      }
    </style>
  </template>
</dom-module>
/* Flexbox alignment */
<dom-module id="iron-flex-alignment">
  <template>
    <style>
      /**
       * Alignment in cross axis.
       */
      .layout.start {
        -ms-flex-align: start;
        -webkit-align-items: flex-start;
        align-items: flex-start;
      }

      .layout.center,
      .layout.center-center {
        -ms-flex-align: center;
        -webkit-align-items: center;
        align-items: center;
      }

      .layout.end {
        -ms-flex-align: end;
        -webkit-align-items: flex-end;
        align-items: flex-end;
      }

      .layout.baseline {
        -ms-flex-align: baseline;
        -webkit-align-items: baseline;
        align-items: baseline;
      }

      /**
       * Alignment in main axis.
       */
      .layout.start-justified {
        -ms-flex-pack: start;
        -webkit-justify-content: flex-start;
        justify-content: flex-start;
      }

      .layout.center-justified,
      .layout.center-center {
        -ms-flex-pack: center;
        -webkit-justify-content: center;
        justify-content: center;
      }

      .layout.end-justified {
        -ms-flex-pack: end;
        -webkit-justify-content: flex-end;
        justify-content: flex-end;
      }

      .layout.around-justified {
        -ms-flex-pack: distribute;
        -webkit-justify-content: space-around;
        justify-content: space-around;
      }

      .layout.justified {
        -ms-flex-pack: justify;
        -webkit-justify-content: space-between;
        justify-content: space-between;
      }

      /**
       * Self alignment.
       */
      .self-start {
        -ms-align-self: flex-start;
        -webkit-align-self: flex-start;
        align-self: flex-start;
      }

      .self-center {
        -ms-align-self: center;
        -webkit-align-self: center;
        align-self: center;
      }

      .self-end {
        -ms-align-self: flex-end;
        -webkit-align-self: flex-end;
        align-self: flex-end;
      }

      .self-stretch {
        -ms-align-self: stretch;
        -webkit-align-self: stretch;
        align-self: stretch;
      }

      .self-baseline {
        -ms-align-self: baseline;
        -webkit-align-self: baseline;
        align-self: baseline;
      }

      /**
       * multi-line alignment in main axis.
       */
      .layout.start-aligned {
        -ms-flex-line-pack: start;  /* IE10 */
        -ms-align-content: flex-start;
        -webkit-align-content: flex-start;
        align-content: flex-start;
      }

      .layout.end-aligned {
        -ms-flex-line-pack: end;  /* IE10 */
        -ms-align-content: flex-end;
        -webkit-align-content: flex-end;
        align-content: flex-end;
      }

      .layout.center-aligned {
        -ms-flex-line-pack: center;  /* IE10 */
        -ms-align-content: center;
        -webkit-align-content: center;
        align-content: center;
      }

      .layout.between-aligned {
        -ms-flex-line-pack: justify;  /* IE10 */
        -ms-align-content: space-between;
        -webkit-align-content: space-between;
        align-content: space-between;
      }

      .layout.around-aligned {
        -ms-flex-line-pack: distribute;  /* IE10 */
        -ms-align-content: space-around;
        -webkit-align-content: space-around;
        align-content: space-around;
      }
    </style>
  </template>
</dom-module>
/* Non-flexbox positioning helper styles */
<dom-module id="iron-flex-factors">
  <template>
    <style>
      .flex,
      .flex-1 {
        -ms-flex: 1 1 0.000000001px;
        -webkit-flex: 1;
        flex: 1;
        -webkit-flex-basis: 0.000000001px;
        flex-basis: 0.000000001px;
      }

      .flex-2 {
        -ms-flex: 2;
        -webkit-flex: 2;
        flex: 2;
      }

      .flex-3 {
        -ms-flex: 3;
        -webkit-flex: 3;
        flex: 3;
      }

      .flex-4 {
        -ms-flex: 4;
        -webkit-flex: 4;
        flex: 4;
      }

      .flex-5 {
        -ms-flex: 5;
        -webkit-flex: 5;
        flex: 5;
      }

      .flex-6 {
        -ms-flex: 6;
        -webkit-flex: 6;
        flex: 6;
      }

      .flex-7 {
        -ms-flex: 7;
        -webkit-flex: 7;
        flex: 7;
      }

      .flex-8 {
        -ms-flex: 8;
        -webkit-flex: 8;
        flex: 8;
      }

      .flex-9 {
        -ms-flex: 9;
        -webkit-flex: 9;
        flex: 9;
      }

      .flex-10 {
        -ms-flex: 10;
        -webkit-flex: 10;
        flex: 10;
      }

      .flex-11 {
        -ms-flex: 11;
        -webkit-flex: 11;
        flex: 11;
      }

      .flex-12 {
        -ms-flex: 12;
        -webkit-flex: 12;
        flex: 12;
      }
    </style>
  </template>
</dom-module>
<dom-module id="iron-positioning">
  <template>
    <style>
      .block {
        display: block;
      }

      [hidden] {
        display: none !important;
      }

      .invisible {
        visibility: hidden !important;
      }

      .relative {
        position: relative;
      }

      .fit {
        position: absolute;
        top: 0;
        right: 0;
        bottom: 0;
        left: 0;
      }

      body.fullbleed {
        margin: 0;
        height: 100vh;
      }

      .scroll {
        -webkit-overflow-scrolling: touch;
        overflow: auto;
      }

      /* fixed position */
      .fixed-bottom,
      .fixed-left,
      .fixed-right,
      .fixed-top {
        position: fixed;
      }

      .fixed-top {
        top: 0;
        left: 0;
        right: 0;
      }

      .fixed-right {
        top: 0;
        right: 0;
        bottom: 0;
      }

      .fixed-bottom {
        right: 0;
        bottom: 0;
        left: 0;
      }

      .fixed-left {
        top: 0;
        bottom: 0;
        left: 0;
      }
    </style>
  </template>
</dom-module>
`;n.setAttribute("style","display: none;"),document.head.appendChild(n.content)},21560:(e,t,l)=>{l.d(t,{ZH:()=>x,MT:()=>s,U2:()=>r,RV:()=>i,t8:()=>f});const n=function(){if(!(!navigator.userAgentData&&/Safari\//.test(navigator.userAgent)&&!/Chrom(e|ium)\//.test(navigator.userAgent))||!indexedDB.databases)return Promise.resolve();let e;return new Promise((t=>{const l=()=>indexedDB.databases().finally(t);e=setInterval(l,100),l()})).finally((()=>clearInterval(e)))};function i(e){return new Promise(((t,l)=>{e.oncomplete=e.onsuccess=()=>t(e.result),e.onabort=e.onerror=()=>l(e.error)}))}function s(e,t){const l=n().then((()=>{const l=indexedDB.open(e);return l.onupgradeneeded=()=>l.result.createObjectStore(t),i(l)}));return(e,n)=>l.then((l=>n(l.transaction(t,e).objectStore(t))))}let o;function a(){return o||(o=s("keyval-store","keyval")),o}function r(e,t=a()){return t("readonly",(t=>i(t.get(e))))}function f(e,t,l=a()){return l("readwrite",(l=>(l.put(t,e),i(l.transaction))))}function x(e=a()){return e("readwrite",(e=>(e.clear(),i(e.transaction))))}},81563:(e,t,l)=>{l.d(t,{E_:()=>p,i9:()=>d,_Y:()=>f,pt:()=>s,OR:()=>a,hN:()=>o,ws:()=>m,fk:()=>x,hl:()=>u});var n=l(15304);const{I:i}=n.Al,s=e=>null===e||"object"!=typeof e&&"function"!=typeof e,o=(e,t)=>void 0===t?void 0!==(null==e?void 0:e._$litType$):(null==e?void 0:e._$litType$)===t,a=e=>void 0===e.strings,r=()=>document.createComment(""),f=(e,t,l)=>{var n;const s=e._$AA.parentNode,o=void 0===t?e._$AB:t._$AA;if(void 0===l){const t=s.insertBefore(r(),o),n=s.insertBefore(r(),o);l=new i(t,n,e,e.options)}else{const t=l._$AB.nextSibling,i=l._$AM,a=i!==e;if(a){let t;null===(n=l._$AQ)||void 0===n||n.call(l,e),l._$AM=e,void 0!==l._$AP&&(t=e._$AU)!==i._$AU&&l._$AP(t)}if(t!==o||a){let e=l._$AA;for(;e!==t;){const t=e.nextSibling;s.insertBefore(e,o),e=t}}}return l},x=(e,t,l=e)=>(e._$AI(t,l),e),c={},u=(e,t=c)=>e._$AH=t,d=e=>e._$AH,m=e=>{var t;null===(t=e._$AP)||void 0===t||t.call(e,!1,!0);let l=e._$AA;const n=e._$AB.nextSibling;for(;l!==n;){const e=l.nextSibling;l.remove(),l=e}},p=e=>{e._$AR()}},86230:(e,t,l)=>{l.d(t,{r:()=>a});var n=l(15304),i=l(38941),s=l(81563);const o=(e,t,l)=>{const n=new Map;for(let i=t;i<=l;i++)n.set(e[i],i);return n},a=(0,i.XM)(class extends i.Xe{constructor(e){if(super(e),e.type!==i.pX.CHILD)throw Error("repeat() can only be used in text expressions")}ht(e,t,l){let n;void 0===l?l=t:void 0!==t&&(n=t);const i=[],s=[];let o=0;for(const t of e)i[o]=n?n(t,o):o,s[o]=l(t,o),o++;return{values:s,keys:i}}render(e,t,l){return this.ht(e,t,l).values}update(e,[t,l,i]){var a;const r=(0,s.i9)(e),{values:f,keys:x}=this.ht(t,l,i);if(!Array.isArray(r))return this.ut=x,f;const c=null!==(a=this.ut)&&void 0!==a?a:this.ut=[],u=[];let d,m,p=0,b=r.length-1,w=0,y=f.length-1;for(;p<=b&&w<=y;)if(null===r[p])p++;else if(null===r[b])b--;else if(c[p]===x[w])u[w]=(0,s.fk)(r[p],f[w]),p++,w++;else if(c[b]===x[y])u[y]=(0,s.fk)(r[b],f[y]),b--,y--;else if(c[p]===x[y])u[y]=(0,s.fk)(r[p],f[y]),(0,s._Y)(e,u[y+1],r[p]),p++,y--;else if(c[b]===x[w])u[w]=(0,s.fk)(r[b],f[w]),(0,s._Y)(e,r[p],r[b]),b--,w++;else if(void 0===d&&(d=o(x,w,y),m=o(c,p,b)),d.has(c[p]))if(d.has(c[b])){const t=m.get(x[w]),l=void 0!==t?r[t]:null;if(null===l){const t=(0,s._Y)(e,r[p]);(0,s.fk)(t,f[w]),u[w]=t}else u[w]=(0,s.fk)(l,f[w]),(0,s._Y)(e,r[p],l),r[t]=null;w++}else(0,s.ws)(r[b]),b--;else(0,s.ws)(r[p]),p++;for(;w<=y;){const t=(0,s._Y)(e,u[y+1]);(0,s.fk)(t,f[w]),u[w++]=t}for(;p<=b;){const e=r[p++];null!==e&&(0,s.ws)(e)}return this.ut=x,(0,s.hl)(e,u),n.Jb}})}}]);
//# sourceMappingURL=67352261.js.map