var LitElement =
  LitElement ||
  Object.getPrototypeOf(customElements.get("home-assistant-main"));
var html = LitElement.prototype.html;

class TextDividerRow extends LitElement {
  static get properties() {
    return {
      _config: {}
    };
  }

  setConfig(config) {
    if (!config || !config.text) {
      throw new Error("Error in card configuration.");
    }

    this._config = config;
  }

  render() {
    if (!this._config) {
      return html``;
    }

    return html`
      ${this.renderStyle()}
      <h2 class="text-divider"><span>${this._config.text}</span></h2>
    `;
  }

  renderStyle() {
    return html`
      <style>
        .text-divider {
          margin: 1em 0;
          line-height: 0;
          text-align: center;
          white-space: nowrap;
          display: flex;
          align-items: center;
        }
        .text-divider span {
          padding: 1em;
          color: var(--secondary-text-color);
        }
        .text-divider:before,
        .text-divider:after  {
          content: '';
          background: var(--secondary-text-color);
          display: block;
          height: 1px;
          width: 100%;
        }
      </style>
    `;
  }
}

customElements.define("text-divider-row", TextDividerRow);
