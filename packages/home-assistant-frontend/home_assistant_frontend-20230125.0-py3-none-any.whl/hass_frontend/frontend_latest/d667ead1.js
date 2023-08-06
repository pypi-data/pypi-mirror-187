/*! For license information please see d667ead1.js.LICENSE.txt */
"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[37232],{63207:(e,t,n)=>{n(65660),n(15112);var r=n(9672),i=n(87156),o=n(50856),a=n(48175);(0,r.k)({_template:o.d`
    <style>
      :host {
        @apply --layout-inline;
        @apply --layout-center-center;
        position: relative;

        vertical-align: middle;

        fill: var(--iron-icon-fill-color, currentcolor);
        stroke: var(--iron-icon-stroke-color, none);

        width: var(--iron-icon-width, 24px);
        height: var(--iron-icon-height, 24px);
        @apply --iron-icon;
      }

      :host([hidden]) {
        display: none;
      }
    </style>
`,is:"iron-icon",properties:{icon:{type:String},theme:{type:String},src:{type:String},_meta:{value:a.XY.create("iron-meta",{type:"iconset"})}},observers:["_updateIcon(_meta, isAttached)","_updateIcon(theme, isAttached)","_srcChanged(src, isAttached)","_iconChanged(icon, isAttached)"],_DEFAULT_ICONSET:"icons",_iconChanged:function(e){var t=(e||"").split(":");this._iconName=t.pop(),this._iconsetName=t.pop()||this._DEFAULT_ICONSET,this._updateIcon()},_srcChanged:function(e){this._updateIcon()},_usesIconset:function(){return this.icon||!this.src},_updateIcon:function(){this._usesIconset()?(this._img&&this._img.parentNode&&(0,i.vz)(this.root).removeChild(this._img),""===this._iconName?this._iconset&&this._iconset.removeIcon(this):this._iconsetName&&this._meta&&(this._iconset=this._meta.byKey(this._iconsetName),this._iconset?(this._iconset.applyIcon(this,this._iconName,this.theme),this.unlisten(window,"iron-iconset-added","_updateIcon")):this.listen(window,"iron-iconset-added","_updateIcon"))):(this._iconset&&this._iconset.removeIcon(this),this._img||(this._img=document.createElement("img"),this._img.style.width="100%",this._img.style.height="100%",this._img.draggable=!1),this._img.src=this.src,(0,i.vz)(this.root).appendChild(this._img))}})},15112:(e,t,n)=>{n.d(t,{P:()=>i});n(48175);var r=n(9672);class i{constructor(e){i[" "](e),this.type=e&&e.type||"default",this.key=e&&e.key,e&&"value"in e&&(this.value=e.value)}get value(){var e=this.type,t=this.key;if(e&&t)return i.types[e]&&i.types[e][t]}set value(e){var t=this.type,n=this.key;t&&n&&(t=i.types[t]=i.types[t]||{},null==e?delete t[n]:t[n]=e)}get list(){if(this.type){var e=i.types[this.type];return e?Object.keys(e).map((function(e){return o[this.type][e]}),this):[]}}byKey(e){return this.key=e,this.value}}i[" "]=function(){},i.types={};var o=i.types;(0,r.k)({is:"iron-meta",properties:{type:{type:String,value:"default"},key:{type:String},value:{type:String,notify:!0},self:{type:Boolean,observer:"_selfChanged"},__meta:{type:Boolean,computed:"__computeMeta(type, key, value)"}},hostAttributes:{hidden:!0},__computeMeta:function(e,t,n){var r=new i({type:e,key:t});return void 0!==n&&n!==r.value?r.value=n:this.value!==r.value&&(this.value=r.value),r},get list(){return this.__meta&&this.__meta.list},_selfChanged:function(e){e&&(this.value=this)},byKey:function(e){return new i({type:this.type,key:e}).value}})},89194:(e,t,n)=>{n(48175),n(65660),n(70019);var r=n(9672),i=n(50856);(0,r.k)({_template:i.d`
    <style>
      :host {
        overflow: hidden; /* needed for text-overflow: ellipsis to work on ff */
        @apply --layout-vertical;
        @apply --layout-center-justified;
        @apply --layout-flex;
      }

      :host([two-line]) {
        min-height: var(--paper-item-body-two-line-min-height, 72px);
      }

      :host([three-line]) {
        min-height: var(--paper-item-body-three-line-min-height, 88px);
      }

      :host > ::slotted(*) {
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
      }

      :host > ::slotted([secondary]) {
        @apply --paper-font-body1;

        color: var(--paper-item-body-secondary-color, var(--secondary-text-color));

        @apply --paper-item-body-secondary;
      }
    </style>

    <slot></slot>
`,is:"paper-item-body"})},23682:(e,t,n)=>{function r(e,t){if(t.length<e)throw new TypeError(e+" argument"+(e>1?"s":"")+" required, but only "+t.length+" present")}n.d(t,{Z:()=>r})},90394:(e,t,n)=>{function r(e){if(null===e||!0===e||!1===e)return NaN;var t=Number(e);return isNaN(t)?t:t<0?Math.ceil(t):Math.floor(t)}n.d(t,{Z:()=>r})},79021:(e,t,n)=>{n.d(t,{Z:()=>a});var r=n(90394),i=n(34327),o=n(23682);function a(e,t){(0,o.Z)(2,arguments);var n=(0,i.Z)(e),a=(0,r.Z)(t);return isNaN(a)?new Date(NaN):a?(n.setDate(n.getDate()+a),n):n}},59699:(e,t,n)=>{n.d(t,{Z:()=>s});var r=n(90394),i=n(39244),o=n(23682),a=36e5;function s(e,t){(0,o.Z)(2,arguments);var n=(0,r.Z)(t);return(0,i.Z)(e,n*a)}},39244:(e,t,n)=>{n.d(t,{Z:()=>a});var r=n(90394),i=n(34327),o=n(23682);function a(e,t){(0,o.Z)(2,arguments);var n=(0,i.Z)(e).getTime(),a=(0,r.Z)(t);return new Date(n+a)}},32182:(e,t,n)=>{n.d(t,{Z:()=>a});var r=n(90394),i=n(34327),o=n(23682);function a(e,t){(0,o.Z)(2,arguments);var n=(0,i.Z)(e),a=(0,r.Z)(t);if(isNaN(a))return new Date(NaN);if(!a)return n;var s=n.getDate(),u=new Date(n.getTime());u.setMonth(n.getMonth()+a+1,0);var l=u.getDate();return s>=l?u:(n.setFullYear(u.getFullYear(),u.getMonth(),s),n)}},4535:(e,t,n)=>{n.d(t,{Z:()=>c});var r=n(34327);function i(e){var t=new Date(Date.UTC(e.getFullYear(),e.getMonth(),e.getDate(),e.getHours(),e.getMinutes(),e.getSeconds(),e.getMilliseconds()));return t.setUTCFullYear(e.getFullYear()),e.getTime()-t.getTime()}var o=n(59429),a=n(23682),s=864e5;function u(e,t){(0,a.Z)(2,arguments);var n=(0,o.Z)(e),r=(0,o.Z)(t),u=n.getTime()-i(n),l=r.getTime()-i(r);return Math.round((u-l)/s)}function l(e,t){var n=e.getFullYear()-t.getFullYear()||e.getMonth()-t.getMonth()||e.getDate()-t.getDate()||e.getHours()-t.getHours()||e.getMinutes()-t.getMinutes()||e.getSeconds()-t.getSeconds()||e.getMilliseconds()-t.getMilliseconds();return n<0?-1:n>0?1:n}function c(e,t){(0,a.Z)(2,arguments);var n=(0,r.Z)(e),i=(0,r.Z)(t),o=l(n,i),s=Math.abs(u(n,i));n.setDate(n.getDate()-o*s);var c=Number(l(n,i)===-o),h=o*(s-c);return 0===h?0:h}},93752:(e,t,n)=>{n.d(t,{Z:()=>o});var r=n(34327),i=n(23682);function o(e){(0,i.Z)(1,arguments);var t=(0,r.Z)(e);return t.setHours(23,59,59,999),t}},70390:(e,t,n)=>{n.d(t,{Z:()=>i});var r=n(93752);function i(){return(0,r.Z)(Date.now())}},47538:(e,t,n)=>{function r(){var e=new Date,t=e.getFullYear(),n=e.getMonth(),r=e.getDate(),i=new Date(0);return i.setFullYear(t,n,r-1),i.setHours(23,59,59,999),i}n.d(t,{Z:()=>r})},59429:(e,t,n)=>{n.d(t,{Z:()=>o});var r=n(34327),i=n(23682);function o(e){(0,i.Z)(1,arguments);var t=(0,r.Z)(e);return t.setHours(0,0,0,0),t}},27088:(e,t,n)=>{n.d(t,{Z:()=>i});var r=n(59429);function i(){return(0,r.Z)(Date.now())}},83008:(e,t,n)=>{function r(){var e=new Date,t=e.getFullYear(),n=e.getMonth(),r=e.getDate(),i=new Date(0);return i.setFullYear(t,n,r-1),i.setHours(0,0,0,0),i}n.d(t,{Z:()=>r})},34327:(e,t,n)=>{n.d(t,{Z:()=>o});var r=n(23682);function i(e){return i="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e},i(e)}function o(e){(0,r.Z)(1,arguments);var t=Object.prototype.toString.call(e);return e instanceof Date||"object"===i(e)&&"[object Date]"===t?new Date(e.getTime()):"number"==typeof e||"[object Number]"===t?new Date(e):("string"!=typeof e&&"[object String]"!==t||"undefined"==typeof console||(console.warn("Starting with v2.0.0-beta.1 date-fns doesn't accept strings as date arguments. Please use `parseISO` to parse strings. See: https://github.com/date-fns/date-fns/blob/master/docs/upgradeGuide.md#string-arguments"),console.warn((new Error).stack)),new Date(NaN))}},21560:(e,t,n)=>{n.d(t,{ZH:()=>c,MT:()=>o,U2:()=>u,RV:()=>i,t8:()=>l});const r=function(){if(!(!navigator.userAgentData&&/Safari\//.test(navigator.userAgent)&&!/Chrom(e|ium)\//.test(navigator.userAgent))||!indexedDB.databases)return Promise.resolve();let e;return new Promise((t=>{const n=()=>indexedDB.databases().finally(t);e=setInterval(n,100),n()})).finally((()=>clearInterval(e)))};function i(e){return new Promise(((t,n)=>{e.oncomplete=e.onsuccess=()=>t(e.result),e.onabort=e.onerror=()=>n(e.error)}))}function o(e,t){const n=r().then((()=>{const n=indexedDB.open(e);return n.onupgradeneeded=()=>n.result.createObjectStore(t),i(n)}));return(e,r)=>n.then((n=>r(n.transaction(t,e).objectStore(t))))}let a;function s(){return a||(a=o("keyval-store","keyval")),a}function u(e,t=s()){return t("readonly",(t=>i(t.get(e))))}function l(e,t,n=s()){return n("readwrite",(n=>(n.put(t,e),i(n.transaction))))}function c(e=s()){return e("readwrite",(e=>(e.clear(),i(e.transaction))))}}}]);
//# sourceMappingURL=d667ead1.js.map