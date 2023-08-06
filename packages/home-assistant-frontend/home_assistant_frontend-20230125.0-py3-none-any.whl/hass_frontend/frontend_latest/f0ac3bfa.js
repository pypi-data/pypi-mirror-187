/*! For license information please see f0ac3bfa.js.LICENSE.txt */
"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[29333],{3239:(e,t,i)=>{function r(e){if(!e||"object"!=typeof e)return e;if("[object Date]"==Object.prototype.toString.call(e))return new Date(e.getTime());if(Array.isArray(e))return e.map(r);var t={};return Object.keys(e).forEach((function(i){t[i]=r(e[i])})),t}i.d(t,{Z:()=>r})},80033:(e,t,i)=>{i.d(t,{xC:()=>r,p4:()=>n,jg:()=>o,pN:()=>s,Dm:()=>a});const r=e=>{let t=e;return"string"==typeof e&&(t=parseInt(e,16)),"0x"+t.toString(16).padStart(4,"0")},n=e=>e.split(":").slice(-4).reverse().join(""),o=(e,t)=>{const i=e.user_given_name?e.user_given_name:e.name,r=t.user_given_name?t.user_given_name:t.name;return i.localeCompare(r)},s=(e,t)=>{const i=e.name,r=t.name;return i.localeCompare(r)},a=e=>`${e.name} (Endpoint id: ${e.endpoint_id}, Id: ${r(e.id)}, Type: ${e.type})`},86444:(e,t,i)=>{i.r(t),i.d(t,{ZHAGroupPage:()=>b});i(51187);var r=i(37500),n=i(36924),o=i(83849),s=(i(31206),i(10983),i(22383)),a=(i(48811),i(60010),i(88165),i(80033));i(79484);function l(){l=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(i){t.forEach((function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var n=t.placement;if(t.kind===r&&("static"===n||"prototype"===n)){var o="static"===n?e:i;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var r=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],r=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!p(e))return i.push(e);var t=this.decorateElement(e,n);i.push(t.element),i.push.apply(i,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:i,finishers:r};var o=this.decorateConstructor(i,t);return r.push.apply(r,o.finishers),o.finishers=r,o},addElementPlacement:function(e,t,i){var r=t[e.placement];if(!i&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var i=[],r=[],n=e.decorators,o=n.length-1;o>=0;o--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[o])(a)||a);e=l.element,this.addElementPlacement(e,t),l.finisher&&r.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);i.push.apply(i,c)}}return{element:e,finishers:r,extras:i}},decorateConstructor:function(e,t){for(var i=[],r=t.length-1;r>=0;r--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[r])(n)||n);if(void 0!==o.finisher&&i.push(o.finisher),void 0!==o.elements){e=o.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return m(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(e):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?m(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=f(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:i,placement:r,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:u(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=u(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var r=(0,t[i])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}function c(e){var t,i=f(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function d(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function p(e){return e.decorators&&e.decorators.length}function h(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function u(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function f(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var r=i.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function m(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,r=new Array(t);i<t;i++)r[i]=e[i];return r}function v(){return v="undefined"!=typeof Reflect&&Reflect.get?Reflect.get.bind():function(e,t,i){var r=y(e,t);if(r){var n=Object.getOwnPropertyDescriptor(r,t);return n.get?n.get.call(arguments.length<3?e:i):n.value}},v.apply(this,arguments)}function y(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=g(e)););return e}function g(e){return g=Object.setPrototypeOf?Object.getPrototypeOf.bind():function(e){return e.__proto__||Object.getPrototypeOf(e)},g(e)}let b=function(e,t,i,r){var n=l();if(r)for(var o=0;o<r.length;o++)n=r[o](n);var s=t((function(e){n.initializeInstanceElements(e,a.elements)}),i),a=n.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},r=0;r<e.length;r++){var n,o=e[r];if("method"===o.kind&&(n=t.find(i)))if(h(o.descriptor)||h(n.descriptor)){if(p(o)||p(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(p(o)){if(p(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}d(o,n)}else t.push(o)}return t}(s.d.map(c)),e);return n.initializeClassElements(s.F,a.elements),n.runClassFinishers(s.F,a.finishers)}([(0,n.Mo)("zha-group-page")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,n.Cb)({type:Object})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.Cb)({type:Object})],key:"group",value:void 0},{kind:"field",decorators:[(0,n.Cb)({type:Number})],key:"groupId",value:void 0},{kind:"field",decorators:[(0,n.Cb)({type:Boolean})],key:"narrow",value:void 0},{kind:"field",decorators:[(0,n.Cb)({type:Boolean})],key:"isWide",value:void 0},{kind:"field",decorators:[(0,n.Cb)({type:Array})],key:"deviceEndpoints",value:()=>[]},{kind:"field",decorators:[(0,n.SB)()],key:"_processingAdd",value:()=>!1},{kind:"field",decorators:[(0,n.SB)()],key:"_processingRemove",value:()=>!1},{kind:"field",decorators:[(0,n.SB)()],key:"_filteredDeviceEndpoints",value:()=>[]},{kind:"field",decorators:[(0,n.SB)()],key:"_selectedDevicesToAdd",value:()=>[]},{kind:"field",decorators:[(0,n.SB)()],key:"_selectedDevicesToRemove",value:()=>[]},{kind:"field",decorators:[(0,n.IO)("#addMembers",!0)],key:"_zhaAddMembersDataTable",value:void 0},{kind:"field",decorators:[(0,n.IO)("#removeMembers")],key:"_zhaRemoveMembersDataTable",value:void 0},{kind:"field",key:"_firstUpdatedCalled",value:()=>!1},{kind:"method",key:"connectedCallback",value:function(){v(g(i.prototype),"connectedCallback",this).call(this),this.hass&&this._firstUpdatedCalled&&this._fetchData()}},{kind:"method",key:"disconnectedCallback",value:function(){v(g(i.prototype),"disconnectedCallback",this).call(this),this._processingAdd=!1,this._processingRemove=!1,this._selectedDevicesToRemove=[],this._selectedDevicesToAdd=[],this.deviceEndpoints=[],this._filteredDeviceEndpoints=[]}},{kind:"method",key:"firstUpdated",value:function(e){v(g(i.prototype),"firstUpdated",this).call(this,e),this.hass&&this._fetchData(),this._firstUpdatedCalled=!0}},{kind:"method",key:"render",value:function(){return this.group?r.dy`
      <hass-subpage
        .hass=${this.hass}
        .narrow=${this.narrow}
        .header=${this.group.name}
      >
        <ha-icon-button
          slot="toolbar-icon"
          .path=${"M19,4H15.5L14.5,3H9.5L8.5,4H5V6H19M6,19A2,2 0 0,0 8,21H16A2,2 0 0,0 18,19V7H6V19Z"}
          @click=${this._deleteGroup}
          .label=${this.hass.localize("ui.panel.config.zha.groups.delete")}
        ></ha-icon-button>
        <ha-config-section .isWide=${this.isWide}>
          <div class="header">
            ${this.hass.localize("ui.panel.config.zha.groups.group_info")}
          </div>

          <p slot="introduction">
            ${this.hass.localize("ui.panel.config.zha.groups.group_details")}
          </p>

          <p><b>Name:</b> ${this.group.name}</p>
          <p><b>Group Id:</b> ${(0,a.xC)(this.group.group_id)}</p>

          <div class="header">
            ${this.hass.localize("ui.panel.config.zha.groups.members")}
          </div>
          <ha-card>
            ${this.group.members.length?this.group.members.map((e=>r.dy`<a
                      href="/config/devices/device/${e.device.device_reg_id}"
                    >
                      <paper-item
                        >${e.device.user_given_name||e.device.name}</paper-item
                      >
                    </a>`)):r.dy` <paper-item> This group has no members </paper-item> `}
          </ha-card>
          ${this.group.members.length?r.dy`
                <div class="header">
                  ${this.hass.localize("ui.panel.config.zha.groups.remove_members")}
                </div>

                <zha-device-endpoint-data-table
                  id="removeMembers"
                  .hass=${this.hass}
                  .deviceEndpoints=${this.group.members}
                  .narrow=${this.narrow}
                  selectable
                  @selection-changed=${this._handleRemoveSelectionChanged}
                >
                </zha-device-endpoint-data-table>

                <div class="buttons">
                  <mwc-button
                    .disabled=${!this._selectedDevicesToRemove.length||this._processingRemove}
                    @click=${this._removeMembersFromGroup}
                    class="button"
                  >
                    <ha-circular-progress
                      ?active=${this._processingRemove}
                      alt=${this.hass.localize("ui.panel.config.zha.groups.removing_members")}
                    ></ha-circular-progress>
                    ${this.hass.localize("ui.panel.config.zha.groups.remove_members")}</mwc-button
                  >
                </div>
              `:r.dy``}

          <div class="header">
            ${this.hass.localize("ui.panel.config.zha.groups.add_members")}
          </div>

          <zha-device-endpoint-data-table
            id="addMembers"
            .hass=${this.hass}
            .deviceEndpoints=${this._filteredDeviceEndpoints}
            .narrow=${this.narrow}
            selectable
            @selection-changed=${this._handleAddSelectionChanged}
          >
          </zha-device-endpoint-data-table>

          <div class="buttons">
            <mwc-button
              .disabled=${!this._selectedDevicesToAdd.length||this._processingAdd}
              @click=${this._addMembersToGroup}
              class="button"
            >
              ${this._processingAdd?r.dy`<ha-circular-progress
                    active
                    size="small"
                    title="Saving"
                  ></ha-circular-progress>`:""}
              ${this.hass.localize("ui.panel.config.zha.groups.add_members")}</mwc-button
            >
          </div>
        </ha-config-section>
      </hass-subpage>
    `:r.dy`
        <hass-error-screen
          .hass=${this.hass}
          .error=${this.hass.localize("ui.panel.config.zha.groups.group_not_found")}
        ></hass-error-screen>
      `}},{kind:"method",key:"_fetchData",value:async function(){null!==this.groupId&&void 0!==this.groupId&&(this.group=await(0,s.yi)(this.hass,this.groupId)),this.deviceEndpoints=await(0,s.pT)(this.hass),this._filterDevices()}},{kind:"method",key:"_filterDevices",value:function(){this._filteredDeviceEndpoints=this.deviceEndpoints.filter((e=>!this.group.members.some((t=>t.device.ieee===e.device.ieee&&t.endpoint_id===e.endpoint_id))))}},{kind:"method",key:"_handleAddSelectionChanged",value:function(e){this._selectedDevicesToAdd=e.detail.value}},{kind:"method",key:"_handleRemoveSelectionChanged",value:function(e){this._selectedDevicesToRemove=e.detail.value}},{kind:"method",key:"_addMembersToGroup",value:async function(){this._processingAdd=!0;const e=this._selectedDevicesToAdd.map((e=>{const t=e.split("_");return{ieee:t[0],endpoint_id:t[1]}}));this.group=await(0,s.dy)(this.hass,this.groupId,e),this._filterDevices(),this._selectedDevicesToAdd=[],this._zhaAddMembersDataTable.clearSelection(),this._processingAdd=!1}},{kind:"method",key:"_removeMembersFromGroup",value:async function(){this._processingRemove=!0;const e=this._selectedDevicesToRemove.map((e=>{const t=e.split("_");return{ieee:t[0],endpoint_id:t[1]}}));this.group=await(0,s.tz)(this.hass,this.groupId,e),this._filterDevices(),this._selectedDevicesToRemove=[],this._zhaRemoveMembersDataTable.clearSelection(),this._processingRemove=!1}},{kind:"method",key:"_deleteGroup",value:async function(){await(0,s.gg)(this.hass,[this.groupId]),(0,o.c)("/config/zha/groups",{replace:!0})}},{kind:"get",static:!0,key:"styles",value:function(){return[r.iv`
        hass-subpage {
          --app-header-text-color: var(--sidebar-icon-color);
        }
        .header {
          font-family: var(--paper-font-display1_-_font-family);
          -webkit-font-smoothing: var(
            --paper-font-display1_-_-webkit-font-smoothing
          );
          font-size: var(--paper-font-display1_-_font-size);
          font-weight: var(--paper-font-display1_-_font-weight);
          letter-spacing: var(--paper-font-display1_-_letter-spacing);
          line-height: var(--paper-font-display1_-_line-height);
          opacity: var(--dark-primary-opacity);
        }

        .button {
          float: right;
        }

        a {
          color: var(--primary-color);
          text-decoration: none;
        }
        .buttons {
          align-items: flex-end;
          padding: 8px;
        }
        .buttons .warning {
          --mdc-theme-primary: var(--error-color);
        }
      `]}}]}}),r.oi)},93217:(e,t,i)=>{i.d(t,{Ud:()=>p});const r=Symbol("Comlink.proxy"),n=Symbol("Comlink.endpoint"),o=Symbol("Comlink.releaseProxy"),s=Symbol("Comlink.thrown"),a=e=>"object"==typeof e&&null!==e||"function"==typeof e,l=new Map([["proxy",{canHandle:e=>a(e)&&e[r],serialize(e){const{port1:t,port2:i}=new MessageChannel;return c(e,t),[i,[i]]},deserialize:e=>(e.start(),p(e))}],["throw",{canHandle:e=>a(e)&&s in e,serialize({value:e}){let t;return t=e instanceof Error?{isError:!0,value:{message:e.message,name:e.name,stack:e.stack}}:{isError:!1,value:e},[t,[]]},deserialize(e){if(e.isError)throw Object.assign(new Error(e.value.message),e.value);throw e.value}}]]);function c(e,t=self){t.addEventListener("message",(function i(n){if(!n||!n.data)return;const{id:o,type:a,path:l}=Object.assign({path:[]},n.data),p=(n.data.argumentList||[]).map(y);let h;try{const t=l.slice(0,-1).reduce(((e,t)=>e[t]),e),i=l.reduce(((e,t)=>e[t]),e);switch(a){case"GET":h=i;break;case"SET":t[l.slice(-1)[0]]=y(n.data.value),h=!0;break;case"APPLY":h=i.apply(t,p);break;case"CONSTRUCT":h=function(e){return Object.assign(e,{[r]:!0})}(new i(...p));break;case"ENDPOINT":{const{port1:t,port2:i}=new MessageChannel;c(e,i),h=function(e,t){return m.set(e,t),e}(t,[t])}break;case"RELEASE":h=void 0;break;default:return}}catch(e){h={value:e,[s]:0}}Promise.resolve(h).catch((e=>({value:e,[s]:0}))).then((e=>{const[r,n]=v(e);t.postMessage(Object.assign(Object.assign({},r),{id:o}),n),"RELEASE"===a&&(t.removeEventListener("message",i),d(t))}))})),t.start&&t.start()}function d(e){(function(e){return"MessagePort"===e.constructor.name})(e)&&e.close()}function p(e,t){return u(e,[],t)}function h(e){if(e)throw new Error("Proxy has been released and is not useable")}function u(e,t=[],i=function(){}){let r=!1;const s=new Proxy(i,{get(i,n){if(h(r),n===o)return()=>g(e,{type:"RELEASE",path:t.map((e=>e.toString()))}).then((()=>{d(e),r=!0}));if("then"===n){if(0===t.length)return{then:()=>s};const i=g(e,{type:"GET",path:t.map((e=>e.toString()))}).then(y);return i.then.bind(i)}return u(e,[...t,n])},set(i,n,o){h(r);const[s,a]=v(o);return g(e,{type:"SET",path:[...t,n].map((e=>e.toString())),value:s},a).then(y)},apply(i,o,s){h(r);const a=t[t.length-1];if(a===n)return g(e,{type:"ENDPOINT"}).then(y);if("bind"===a)return u(e,t.slice(0,-1));const[l,c]=f(s);return g(e,{type:"APPLY",path:t.map((e=>e.toString())),argumentList:l},c).then(y)},construct(i,n){h(r);const[o,s]=f(n);return g(e,{type:"CONSTRUCT",path:t.map((e=>e.toString())),argumentList:o},s).then(y)}});return s}function f(e){const t=e.map(v);return[t.map((e=>e[0])),(i=t.map((e=>e[1])),Array.prototype.concat.apply([],i))];var i}const m=new WeakMap;function v(e){for(const[t,i]of l)if(i.canHandle(e)){const[r,n]=i.serialize(e);return[{type:"HANDLER",name:t,value:r},n]}return[{type:"RAW",value:e},m.get(e)||[]]}function y(e){switch(e.type){case"HANDLER":return l.get(e.name).deserialize(e.value);case"RAW":return e.value}}function g(e,t,i){return new Promise((r=>{const n=new Array(4).fill(0).map((()=>Math.floor(Math.random()*Number.MAX_SAFE_INTEGER).toString(16))).join("-");e.addEventListener("message",(function t(i){i.data&&i.data.id&&i.data.id===n&&(e.removeEventListener("message",t),r(i.data))})),e.start&&e.start(),e.postMessage(Object.assign({id:n},t),i)}))}},19596:(e,t,i)=>{i.d(t,{sR:()=>p});var r=i(81563),n=i(38941);const o=(e,t)=>{var i,r;const n=e._$AN;if(void 0===n)return!1;for(const e of n)null===(r=(i=e)._$AO)||void 0===r||r.call(i,t,!1),o(e,t);return!0},s=e=>{let t,i;do{if(void 0===(t=e._$AM))break;i=t._$AN,i.delete(e),e=t}while(0===(null==i?void 0:i.size))},a=e=>{for(let t;t=e._$AM;e=t){let i=t._$AN;if(void 0===i)t._$AN=i=new Set;else if(i.has(e))break;i.add(e),d(t)}};function l(e){void 0!==this._$AN?(s(this),this._$AM=e,a(this)):this._$AM=e}function c(e,t=!1,i=0){const r=this._$AH,n=this._$AN;if(void 0!==n&&0!==n.size)if(t)if(Array.isArray(r))for(let e=i;e<r.length;e++)o(r[e],!1),s(r[e]);else null!=r&&(o(r,!1),s(r));else o(this,e)}const d=e=>{var t,i,r,o;e.type==n.pX.CHILD&&(null!==(t=(r=e)._$AP)&&void 0!==t||(r._$AP=c),null!==(i=(o=e)._$AQ)&&void 0!==i||(o._$AQ=l))};class p extends n.Xe{constructor(){super(...arguments),this._$AN=void 0}_$AT(e,t,i){super._$AT(e,t,i),a(this),this.isConnected=e._$AU}_$AO(e,t=!0){var i,r;e!==this.isConnected&&(this.isConnected=e,e?null===(i=this.reconnected)||void 0===i||i.call(this):null===(r=this.disconnected)||void 0===r||r.call(this)),t&&(o(this,e),s(this))}setValue(e){if((0,r.OR)(this._$Ct))this._$Ct._$AI(e,this);else{const t=[...this._$Ct._$AH];t[this._$Ci]=e,this._$Ct._$AI(t,this,0)}}disconnected(){}reconnected(){}}},81563:(e,t,i)=>{i.d(t,{E_:()=>m,i9:()=>u,_Y:()=>c,pt:()=>o,OR:()=>a,hN:()=>s,ws:()=>f,fk:()=>d,hl:()=>h});var r=i(15304);const{I:n}=r.Al,o=e=>null===e||"object"!=typeof e&&"function"!=typeof e,s=(e,t)=>void 0===t?void 0!==(null==e?void 0:e._$litType$):(null==e?void 0:e._$litType$)===t,a=e=>void 0===e.strings,l=()=>document.createComment(""),c=(e,t,i)=>{var r;const o=e._$AA.parentNode,s=void 0===t?e._$AB:t._$AA;if(void 0===i){const t=o.insertBefore(l(),s),r=o.insertBefore(l(),s);i=new n(t,r,e,e.options)}else{const t=i._$AB.nextSibling,n=i._$AM,a=n!==e;if(a){let t;null===(r=i._$AQ)||void 0===r||r.call(i,e),i._$AM=e,void 0!==i._$AP&&(t=e._$AU)!==n._$AU&&i._$AP(t)}if(t!==s||a){let e=i._$AA;for(;e!==t;){const t=e.nextSibling;o.insertBefore(e,s),e=t}}}return i},d=(e,t,i=e)=>(e._$AI(t,i),e),p={},h=(e,t=p)=>e._$AH=t,u=e=>e._$AH,f=e=>{var t;null===(t=e._$AP)||void 0===t||t.call(e,!1,!0);let i=e._$AA;const r=e._$AB.nextSibling;for(;i!==r;){const e=i.nextSibling;i.remove(),i=e}},m=e=>{e._$AR()}}}]);
//# sourceMappingURL=f0ac3bfa.js.map