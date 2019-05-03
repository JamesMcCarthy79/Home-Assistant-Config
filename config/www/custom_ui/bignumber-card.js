class BigNumberCard extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
  }
  setConfig(config) {
    if (!config.entity) {
      throw new Error('Please define an entity');
    }

    const root = this.shadowRoot;
    if (root.lastChild) root.removeChild(root.lastChild);
    const cardConfig = Object.assign({}, config);
    if (!cardConfig.scale) cardConfig.scale = "50px";
    if (!cardConfig.from) cardConfig.from = "left";
    const card = document.createElement('ha-card');
    const content = document.createElement('div');
    content.id = "value"
    const title = document.createElement('div');
    title.id = "title"
    title.textContent = cardConfig.title;
    const style = document.createElement('style');
    style.textContent = `
      ha-card {
        text-align: center;
        --bignumber-fill-color: var(--label-badge-blue);
        --bignumber-percent: 100%;
        --bignumber-direction: ${cardConfig.from};
        --base-unit: ${cardConfig.scale};
        padding: calc(var(--base-unit)*0.6) calc(var(--base-unit)*0.3);
        background: linear-gradient(to var(--bignumber-direction), var(--paper-card-background-color) var(--bignumber-percent), var(--bignumber-fill-color) var(--bignumber-percent));
      }
      #value {
        font-size: calc(var(--base-unit) * 1.3);
        line-height: calc(var(--base-unit) * 1.3);
        color: var(--primary-text-color);
      }
      #title {
        font-size: calc(var(--base-unit) * 0.5);
        line-height: calc(var(--base-unit) * 0.5);
        color: var(--primary-text-color);
      }
    `;
    card.appendChild(content);
    card.appendChild(title);
    card.appendChild(style);
    card.addEventListener('click', event => {
      this._fire('hass-more-info', { entityId: cardConfig.entity });
    });
    root.appendChild(card);
    this._config = cardConfig;
  }

  _fire(type, detail, options) {
    const node = this.shadowRoot;
    options = options || {};
    detail = (detail === null || detail === undefined) ? {} : detail;
    const event = new Event(type, {
      bubbles: options.bubbles === undefined ? true : options.bubbles,
      cancelable: Boolean(options.cancelable),
      composed: options.composed === undefined ? true : options.composed
    });
    event.detail = detail;
    node.dispatchEvent(event);
    return event;
  }

  _computeSeverity(stateValue, sections) {
    const numberValue = Number(stateValue);
    let style;
    sections.forEach(section => {
      if (numberValue <= section.value && !style) {
        style = section.style;
      }
    });
    return style || 'var(--label-badge-blue)';
  }

  _translatePercent(value, min, max) {
    return 100-100 * (value - min) / (max - min);
  }

  set hass(hass) {
    const config = this._config;
    const root = this.shadowRoot;
    const entityState = hass.states[config.entity].state;
    const measurement = hass.states[config.entity].attributes.unit_of_measurement || "";

    if (entityState !== this._entityState) {
      if (config.min !== undefined && config.max !== undefined) {
        root.querySelector("ha-card").style.setProperty('--bignumber-percent', `${this._translatePercent(entityState, config.min, config.max)}%`);
      }
      if (config.severity) {
        root.querySelector("ha-card").style.setProperty('--bignumber-fill-color', `${this._computeSeverity(entityState, config.severity)}`);
      }
      root.getElementById("value").textContent = `${entityState} ${measurement}`;
      this._entityState = entityState
    }
    root.lastChild.hass = hass;
  }

  getCardSize() {
    return 1;
  }
}

customElements.define('bignumber-card', BigNumberCard);