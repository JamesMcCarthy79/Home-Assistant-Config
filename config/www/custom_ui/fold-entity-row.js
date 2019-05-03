customElements.whenDefined('card-tools').then(() => {
let cardTools = customElements.get('card-tools');
class FoldEntityRow extends cardTools.LitElement {

  static get properties() {
    return {
      _closed: Boolean,
    };
  }

  render() {
    return cardTools.LitHtml`
    ${this._renderStyle()}
    <div id=head>
      <div id=entity>
        ${this._head}
      </div>
      <div id=toggle>
        <ha-icon @click=${this._toggle} icon="${this._closed ? "mdi:chevron-down" : "mdi:chevron-up"}"></ha-icon>
      </div>
    </div>
    <div id=items ?closed=${this._closed}>
      ${this._entities}
    </div>
    `;
  }

  _renderStyle() {
    return cardTools.LitHtml`
    <style>
    #items {
      padding: 0 0 0 40px;
      margin: 0;
    }
    [closed] > div {
      overflow: hidden;
      max-height: 0;
    }
    #head {
      display: flex;
    }
    #entity {
      flex: 1 1 auto;
      width: 0px;
    }
    #toggle {
      flex: 0 1 40px;
      display: flex;
      align-items: center;
    }
    ha-icon {
      width: 40px;
    }
    </style>
    `;
  }


  firstUpdated() {
    this.hass = this._hass;
  }

  _toggle()
  {
    this._closed = !this._closed;
  }

  _renderElement(conf, options) {
    conf = (typeof conf === "string") ? {entity: conf} : conf;
    conf = Object.assign(conf, options);
    const element = cardTools.createEntityRow(conf);
    if(this._hass) element.hass = this._hass;

    const DOMAINS_HIDE_MORE_INFO = [
      "input_number",
      "input_select",
      "input_text",
      "scene",
      "weblink",
    ];
    if (conf.entity && !DOMAINS_HIDE_MORE_INFO.includes(conf.entity.split(".")[0])) {
      element.classList.add("state-card-dialog");
      element.addEventListener("click", () => {
        cardTools.moreInfo(conf.entity);
      });
    }
    return element;
  }

  _renderHead(conf) {
    const element = this._renderElement(conf);

    // Stretch the line above section rows
    if (conf.type && conf.type === "section") {
      element.updateComplete.then(() => {
        const divider = element.shadowRoot.querySelector(".divider");
        divider.style.marginRight = "-53px";
      });
    }
    return element;
  }

  _renderItem(conf, options) {
    const element = this._renderElement(conf, options);
    return cardTools.LitHtml`<div> ${element} </div>`;
  }

  setConfig(config) {
    if(!this._config) {
      if(!cardTools) throw new Error(`Can't find card-tools. See https://github.com/thomasloven/lovelace-card-tools`);
      cardTools.checkVersion(0.1);
      this._config = config;
      this._closed = !config.open;

      this._head = this._renderHead(config.head);
    }

    const head = (typeof config.head === "string") ? config.head : config.head.entity;
    let items = config.items
    if (config.entities)
      items = config.entities;
    if (head && head.split('.')[0] === "group")
      items = cardTools.hass.states[head].attributes.entity_id;

    if(items)
      this._entities = items.map((e) => this._renderItem(e, config.group_config));
    this.requestUpdate();
  }

  set hass(hass) {
    this._hass = hass;
    this._head.hass = hass;
    this.shadowRoot.querySelectorAll("#items > div > *").forEach((e) => e.hass = hass);
  }
}

customElements.define('fold-entity-row', FoldEntityRow);
});

window.setTimeout(() => {
  if(customElements.get('card-tools')) return;
  customElements.define('fold-entity-row', class extends HTMLElement{
    setConfig() { throw new Error("Can't find card-tools. See https://github.com/thomasloven/lovelace-card-tools");}
  });
}, 2000);
