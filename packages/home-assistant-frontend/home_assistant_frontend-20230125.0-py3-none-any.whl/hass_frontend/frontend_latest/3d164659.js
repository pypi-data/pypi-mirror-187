/*! For license information please see 3d164659.js.LICENSE.txt */
"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[69439],{26765:(e,t,i)=>{i.d(t,{Ys:()=>s,g7:()=>a,D9:()=>l});var r=i(47181);const n=()=>Promise.all([i.e(85084),i.e(1281)]).then(i.bind(i,1281)),o=(e,t,i)=>new Promise((o=>{const s=t.cancel,a=t.confirm;(0,r.B)(e,"show-dialog",{dialogTag:"dialog-box",dialogImport:n,dialogParams:{...t,...i,cancel:()=>{o(!(null==i||!i.prompt)&&null),s&&s()},confirm:e=>{o(null==i||!i.prompt||e),a&&a(e)}}})})),s=(e,t)=>o(e,t),a=(e,t)=>o(e,t,{confirmation:!0}),l=(e,t)=>o(e,t,{prompt:!0})},51444:(e,t,i)=>{i.d(t,{_:()=>o});var r=i(47181);const n=()=>Promise.all([i.e(98985),i.e(85084),i.e(39928)]).then(i.bind(i,39928)),o=e=>{(0,r.B)(e,"show-dialog",{dialogTag:"ha-voice-command-dialog",dialogImport:n,dialogParams:{}})}},27849:(e,t,i)=>{i(39841);var r=i(50856);i(28426);class n extends(customElements.get("app-header-layout")){static get template(){return r.d`
      <style>
        :host {
          display: block;
          /**
         * Force app-header-layout to have its own stacking context so that its parent can
         * control the stacking of it relative to other elements (e.g. app-drawer-layout).
         * This could be done using \`isolation: isolate\`, but that's not well supported
         * across browsers.
         */
          position: relative;
          z-index: 0;
        }

        #wrapper ::slotted([slot="header"]) {
          @apply --layout-fixed-top;
          z-index: 1;
        }

        #wrapper.initializing ::slotted([slot="header"]) {
          position: relative;
        }

        :host([has-scrolling-region]) {
          height: 100%;
        }

        :host([has-scrolling-region]) #wrapper ::slotted([slot="header"]) {
          position: absolute;
        }

        :host([has-scrolling-region])
          #wrapper.initializing
          ::slotted([slot="header"]) {
          position: relative;
        }

        :host([has-scrolling-region]) #wrapper #contentContainer {
          @apply --layout-fit;
          overflow-y: auto;
          -webkit-overflow-scrolling: touch;
        }

        :host([has-scrolling-region]) #wrapper.initializing #contentContainer {
          position: relative;
        }

        #contentContainer {
          /* Create a stacking context here so that all children appear below the header. */
          position: relative;
          z-index: 0;
          /* Using 'transform' will cause 'position: fixed' elements to behave like
           'position: absolute' relative to this element. */
          transform: translate(0);
          margin-left: env(safe-area-inset-left);
          margin-right: env(safe-area-inset-right);
          padding-top: env(safe-area-inset-top);
          padding-bottom: env(safe-area-inset-bottom);
        }

        @media print {
          :host([has-scrolling-region]) #wrapper #contentContainer {
            overflow-y: visible;
          }
        }
      </style>

      <div id="wrapper" class="initializing">
        <slot id="headerSlot" name="header"></slot>

        <div id="contentContainer"><slot></slot></div>
        <slot id="fab" name="fab"></slot>
      </div>
    `}}customElements.define("ha-app-layout",n)},51153:(e,t,i)=>{i.a(e,(async e=>{i.d(t,{l$:()=>g,Z6:()=>b,Do:()=>w});var r=i(10175),n=(i(80251),i(89894)),o=i(14888),s=i(69377),a=i(95035),l=i(6169),d=i(41043),c=i(57464),h=i(24617),p=i(82778),u=i(22720),f=i(7778),m=e([u,p,h,c,d,l,a,s,o,n,r]);[u,p,h,c,d,l,a,s,o,n,r]=m.then?await m:m;const v=new Set(["entity","entities","button","entity-button","glance","grid","light","sensor","thermostat","weather-forecast","tile"]),y={"alarm-panel":()=>Promise.all([i.e(98985),i.e(77639)]).then(i.bind(i,77639)),area:()=>Promise.all([i.e(97282),i.e(95795)]).then(i.bind(i,95795)),calendar:()=>Promise.resolve().then(i.bind(i,80251)),conditional:()=>i.e(68857).then(i.bind(i,68857)),"empty-state":()=>i.e(67284).then(i.bind(i,67284)),"energy-compare":()=>i.e(61046).then(i.bind(i,61046)),"energy-carbon-consumed-gauge":()=>Promise.all([i.e(21233),i.e(49915),i.e(43283),i.e(19490)]).then(i.bind(i,19490)),"energy-date-selection":()=>Promise.all([i.e(23754),i.e(2937)]).then(i.bind(i,10346)),"energy-devices-graph":()=>Promise.all([i.e(1671),i.e(62336),i.e(94576)]).then(i.bind(i,94576)),"energy-distribution":()=>i.e(9928).then(i.bind(i,9928)),"energy-gas-graph":()=>Promise.all([i.e(62336),i.e(41305)]).then(i.bind(i,41305)),"energy-water-graph":()=>Promise.all([i.e(62336),i.e(89127)]).then(i.bind(i,89127)),"energy-grid-neutrality-gauge":()=>Promise.all([i.e(64101),i.e(49915),i.e(32176)]).then(i.bind(i,32176)),"energy-solar-consumed-gauge":()=>Promise.all([i.e(66601),i.e(49915),i.e(43283),i.e(85930)]).then(i.bind(i,85930)),"energy-solar-graph":()=>Promise.all([i.e(62336),i.e(70310)]).then(i.bind(i,70310)),"energy-sources-table":()=>Promise.all([i.e(40299),i.e(16938)]).then(i.bind(i,16938)),"energy-usage-graph":()=>Promise.all([i.e(62336),i.e(9897)]).then(i.bind(i,9897)),"entity-filter":()=>i.e(33688).then(i.bind(i,33688)),error:()=>Promise.all([i.e(77426),i.e(55796)]).then(i.bind(i,55796)),gauge:()=>Promise.all([i.e(49915),i.e(43283)]).then(i.bind(i,43283)),"history-graph":()=>Promise.all([i.e(26545),i.e(62336),i.e(25825),i.e(88171)]).then(i.bind(i,38026)),"horizontal-stack":()=>i.e(89173).then(i.bind(i,89173)),humidifier:()=>i.e(68558).then(i.bind(i,68558)),iframe:()=>i.e(95018).then(i.bind(i,95018)),logbook:()=>Promise.all([i.e(99528),i.e(40967),i.e(90851)]).then(i.bind(i,8436)),map:()=>Promise.all([i.e(23956),i.e(60076)]).then(i.bind(i,60076)),markdown:()=>Promise.all([i.e(4940),i.e(26607)]).then(i.bind(i,51282)),"media-control":()=>Promise.all([i.e(28611),i.e(11866)]).then(i.bind(i,11866)),"picture-elements":()=>Promise.all([i.e(97282),i.e(54909),i.e(99810),i.e(15476)]).then(i.bind(i,83358)),"picture-entity":()=>Promise.all([i.e(97282),i.e(41500)]).then(i.bind(i,41500)),"picture-glance":()=>Promise.all([i.e(97282),i.e(66621)]).then(i.bind(i,66621)),picture:()=>i.e(45338).then(i.bind(i,45338)),"plant-status":()=>i.e(48723).then(i.bind(i,48723)),"safe-mode":()=>Promise.all([i.e(47398),i.e(24503)]).then(i.bind(i,24503)),"shopping-list":()=>Promise.all([i.e(98985),i.e(41985),i.e(43376)]).then(i.bind(i,43376)),starting:()=>i.e(47873).then(i.bind(i,47873)),"statistics-graph":()=>Promise.all([i.e(62336),i.e(95396)]).then(i.bind(i,95396)),statistic:()=>i.e(99897).then(i.bind(i,99897)),"vertical-stack":()=>i.e(26136).then(i.bind(i,26136))},g=e=>(0,f.Xm)("card",e,v,y,void 0,void 0),b=e=>(0,f.Tw)("card",e,v,y,void 0,void 0),w=e=>(0,f.ED)(e,"card",v,y)}))},89026:(e,t,i)=>{i.d(t,{t:()=>o,Q:()=>s});var r=i(7778);const n={picture:()=>i.e(69130).then(i.bind(i,69130)),buttons:()=>Promise.all([i.e(42109),i.e(32587)]).then(i.bind(i,32587)),graph:()=>i.e(23256).then(i.bind(i,28922))},o=e=>(0,r.Tw)("header-footer",e,void 0,n,void 0,void 0),s=e=>(0,r.ED)(e,"header-footer",void 0,n)},44295:(e,t,i)=>{i.a(e,(async e=>{i.r(t);i(53268),i(12730);var r=i(37500),n=i(36924),o=i(14516),s=i(7323),a=(i(10983),i(48932),i(51444)),l=(i(27849),i(11654)),d=i(51153),c=e([d]);function h(){h=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(i){t.forEach((function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var n=t.placement;if(t.kind===r&&("static"===n||"prototype"===n)){var o="static"===n?e:i;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var r=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],r=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!f(e))return i.push(e);var t=this.decorateElement(e,n);i.push(t.element),i.push.apply(i,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:i,finishers:r};var o=this.decorateConstructor(i,t);return r.push.apply(r,o.finishers),o.finishers=r,o},addElementPlacement:function(e,t,i){var r=t[e.placement];if(!i&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var i=[],r=[],n=e.decorators,o=n.length-1;o>=0;o--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[o])(a)||a);e=l.element,this.addElementPlacement(e,t),l.finisher&&r.push(l.finisher);var d=l.extras;if(d){for(var c=0;c<d.length;c++)this.addElementPlacement(d[c],t);i.push.apply(i,d)}}return{element:e,finishers:r,extras:i}},decorateConstructor:function(e,t){for(var i=[],r=t.length-1;r>=0;r--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[r])(n)||n);if(void 0!==o.finisher&&i.push(o.finisher),void 0!==o.elements){e=o.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return g(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(e):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?g(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=y(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:i,placement:r,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:v(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=v(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var r=(0,t[i])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}function p(e){var t,i=y(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function u(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function f(e){return e.decorators&&e.decorators.length}function m(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function v(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function y(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var r=i.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function g(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,r=new Array(t);i<t;i++)r[i]=e[i];return r}function b(){return b="undefined"!=typeof Reflect&&Reflect.get?Reflect.get.bind():function(e,t,i){var r=w(e,t);if(r){var n=Object.getOwnPropertyDescriptor(r,t);return n.get?n.get.call(arguments.length<3?e:i):n.value}},b.apply(this,arguments)}function w(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=k(e)););return e}function k(e){return k=Object.setPrototypeOf?Object.getPrototypeOf.bind():function(e){return e.__proto__||Object.getPrototypeOf(e)},k(e)}d=(c.then?await c:c)[0];!function(e,t,i,r){var n=h();if(r)for(var o=0;o<r.length;o++)n=r[o](n);var s=t((function(e){n.initializeInstanceElements(e,a.elements)}),i),a=n.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},r=0;r<e.length;r++){var n,o=e[r];if("method"===o.kind&&(n=t.find(i)))if(m(o.descriptor)||m(n.descriptor)){if(f(o)||f(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(f(o)){if(f(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}u(o,n)}else t.push(o)}return t}(s.d.map(p)),e);n.initializeClassElements(s.F,a.elements),n.runClassFinishers(s.F,a.finishers)}([(0,n.Mo)("ha-panel-shopping-list")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.Cb)({type:Boolean,reflect:!0})],key:"narrow",value:void 0},{kind:"field",decorators:[(0,n.SB)()],key:"_card",value:void 0},{kind:"field",key:"_conversation",value(){return(0,o.Z)((e=>(0,s.p)(this.hass,"conversation")))}},{kind:"method",key:"firstUpdated",value:function(e){b(k(i.prototype),"firstUpdated",this).call(this,e),this._card=(0,d.Z6)({type:"shopping-list"}),this._card.hass=this.hass}},{kind:"method",key:"updated",value:function(e){b(k(i.prototype),"updated",this).call(this,e),e.has("hass")&&(this._card.hass=this.hass)}},{kind:"method",key:"render",value:function(){return r.dy`
      <ha-app-layout>
        <app-header fixed slot="header">
          <app-toolbar>
            <ha-menu-button
              .hass=${this.hass}
              .narrow=${this.narrow}
            ></ha-menu-button>
            <div main-title>${this.hass.localize("panel.shopping_list")}</div>
            ${this._conversation(this.hass.config.components)?r.dy`
                  <ha-icon-button
                    .label=${this.hass.localize("ui.panel.shopping_list.start_conversation")}
                    .path=${"M12,2A3,3 0 0,1 15,5V11A3,3 0 0,1 12,14A3,3 0 0,1 9,11V5A3,3 0 0,1 12,2M19,11C19,14.53 16.39,17.44 13,17.93V21H11V17.93C7.61,17.44 5,14.53 5,11H7A5,5 0 0,0 12,16A5,5 0 0,0 17,11H19Z"}
                    @click=${this._showVoiceCommandDialog}
                  ></ha-icon-button>
                `:""}
          </app-toolbar>
        </app-header>
        <div id="columns">
          <div class="column">${this._card}</div>
        </div>
      </ha-app-layout>
    `}},{kind:"method",key:"_showVoiceCommandDialog",value:function(){(0,a._)(this)}},{kind:"get",static:!0,key:"styles",value:function(){return[l.Qx,r.iv`
        :host {
          display: block;
          height: 100%;
        }
        app-header {
          --mdc-theme-primary: var(--app-header-text-color);
        }
        :host([narrow]) app-toolbar mwc-button {
          width: 65px;
        }
        .heading {
          overflow: hidden;
          white-space: nowrap;
          margin-top: 4px;
        }
        #columns {
          display: flex;
          flex-direction: row;
          justify-content: center;
          margin-left: 4px;
          margin-right: 4px;
        }
        .column {
          flex: 1 0 0;
          max-width: 500px;
          min-width: 0;
        }
      `]}}]}}),r.oi)}))},19596:(e,t,i)=>{i.d(t,{sR:()=>h});var r=i(81563),n=i(38941);const o=(e,t)=>{var i,r;const n=e._$AN;if(void 0===n)return!1;for(const e of n)null===(r=(i=e)._$AO)||void 0===r||r.call(i,t,!1),o(e,t);return!0},s=e=>{let t,i;do{if(void 0===(t=e._$AM))break;i=t._$AN,i.delete(e),e=t}while(0===(null==i?void 0:i.size))},a=e=>{for(let t;t=e._$AM;e=t){let i=t._$AN;if(void 0===i)t._$AN=i=new Set;else if(i.has(e))break;i.add(e),c(t)}};function l(e){void 0!==this._$AN?(s(this),this._$AM=e,a(this)):this._$AM=e}function d(e,t=!1,i=0){const r=this._$AH,n=this._$AN;if(void 0!==n&&0!==n.size)if(t)if(Array.isArray(r))for(let e=i;e<r.length;e++)o(r[e],!1),s(r[e]);else null!=r&&(o(r,!1),s(r));else o(this,e)}const c=e=>{var t,i,r,o;e.type==n.pX.CHILD&&(null!==(t=(r=e)._$AP)&&void 0!==t||(r._$AP=d),null!==(i=(o=e)._$AQ)&&void 0!==i||(o._$AQ=l))};class h extends n.Xe{constructor(){super(...arguments),this._$AN=void 0}_$AT(e,t,i){super._$AT(e,t,i),a(this),this.isConnected=e._$AU}_$AO(e,t=!0){var i,r;e!==this.isConnected&&(this.isConnected=e,e?null===(i=this.reconnected)||void 0===i||i.call(this):null===(r=this.disconnected)||void 0===r||r.call(this)),t&&(o(this,e),s(this))}setValue(e){if((0,r.OR)(this._$Ct))this._$Ct._$AI(e,this);else{const t=[...this._$Ct._$AH];t[this._$Ci]=e,this._$Ct._$AI(t,this,0)}}disconnected(){}reconnected(){}}},81563:(e,t,i)=>{i.d(t,{E_:()=>m,i9:()=>u,_Y:()=>d,pt:()=>o,OR:()=>a,hN:()=>s,ws:()=>f,fk:()=>c,hl:()=>p});var r=i(15304);const{I:n}=r.Al,o=e=>null===e||"object"!=typeof e&&"function"!=typeof e,s=(e,t)=>void 0===t?void 0!==(null==e?void 0:e._$litType$):(null==e?void 0:e._$litType$)===t,a=e=>void 0===e.strings,l=()=>document.createComment(""),d=(e,t,i)=>{var r;const o=e._$AA.parentNode,s=void 0===t?e._$AB:t._$AA;if(void 0===i){const t=o.insertBefore(l(),s),r=o.insertBefore(l(),s);i=new n(t,r,e,e.options)}else{const t=i._$AB.nextSibling,n=i._$AM,a=n!==e;if(a){let t;null===(r=i._$AQ)||void 0===r||r.call(i,e),i._$AM=e,void 0!==i._$AP&&(t=e._$AU)!==n._$AU&&i._$AP(t)}if(t!==s||a){let e=i._$AA;for(;e!==t;){const t=e.nextSibling;o.insertBefore(e,s),e=t}}}return i},c=(e,t,i=e)=>(e._$AI(t,i),e),h={},p=(e,t=h)=>e._$AH=t,u=e=>e._$AH,f=e=>{var t;null===(t=e._$AP)||void 0===t||t.call(e,!1,!0);let i=e._$AA;const r=e._$AB.nextSibling;for(;i!==r;){const e=i.nextSibling;i.remove(),i=e}},m=e=>{e._$AR()}}}]);
//# sourceMappingURL=3d164659.js.map