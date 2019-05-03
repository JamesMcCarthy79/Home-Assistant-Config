customElements.whenDefined('card-tools').then(() => {
let cardTools = customElements.get('card-tools');
class UsefulMarkdownCard extends cardTools.LitElement {

  async setConfig(config) {
    this._config = config;
    this.cardConfig = Object.assign({
      type: "markdown",
    },
      config);
    this.cardConfig.type = "markdown";
    this.update_content();
    window.addEventListener("location-changed", () => this.update_content() );
  }

  render() {
    return cardTools.LitHtml`
    <div id="root">${this.card}</div>
    `;
  }

  getCardSize()
  {
    if(!this.card) return 1;
    return this.card.getCardSize ? this.card.getCardSize() : 1;
  }

  async update_content() {
    const newContent = cardTools.parseTemplate(this._config.content);
    if(newContent != this.oldContent) {
      this.oldContent = newContent;
      this.cardConfig.content = newContent;
      if(!this.card)
        this.card = cardTools.createCard(this.cardConfig);
      else
        this.card.setConfig(this.cardConfig);
      if(this.card.requestUpdate)
        this.card.requestUpdate();
    }
  }

  set hass(hass) {
    this._hass = hass;
    this.update_content()
  }
}

customElements.define('useful-markdown-card', UsefulMarkdownCard);
});

window.setTimeout(() => {
  if(customElements.get('card-tools')) return;
  customElements.define('useful-markdown-card', class extends HTMLElement{
    setConfig() { throw new Error("Can't find card-tools. See https://github.com/thomasloven/lovelace-card-tools");}
  });
}, 2000);