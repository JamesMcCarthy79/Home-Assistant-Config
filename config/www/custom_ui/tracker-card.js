class TrackerCard extends HTMLElement {

  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
  }

  setConfig(config) {
    if (!config.trackers || !Array.isArray(config.trackers)) {
      throw new Error('Please at least one tracker');
    }

    const root = this.shadowRoot;
    if (root.lastChild) root.removeChild(root.lastChild);

    const cardConfig = Object.assign({}, config);
    if (!cardConfig.title) {
      cardConfig.title = '📣 Updates';
    } else {
      cardConfig.title = '📣 ' + cardConfig.title;
    }
    const card = document.createElement('ha-card');
    const content = document.createElement('div');
    const style = document.createElement('style');
    style.textContent = `
          ha-card {
            /* sample css */
          }
          table {
            width: 100%;
            padding: 0 32px 0 32px;
          }
          thead th {
            text-align: left;
          }
          tbody tr:nth-child(odd) {
            background-color: var(--paper-card-background-color);
          }
          tbody tr:nth-child(even) {
            background-color: var(--secondary-background-color);
          }
          .button {
            overflow: auto;
            padding: 16px;
          }
          paper-button {
            float: right;
          }
          tbody td.name a {
            color: var(--primary-text-color);
            text-decoration-line: none;
            font-weight: normal;
          }
          td a {
            color: red;
            font-weight: bold;
          }
          tbody td.separator {
            font-weight: bold;
            padding-top: 10px;
            text-transform: capitalize;
          }
        `;
    content.innerHTML = `
      <div id='content'>
      </div>
      <div class='button'>
        <paper-button raised id='update'>Update All</paper-button>
        <paper-button raised id='check'>Check</paper-button>
      </div>
    `;
    card.header = cardConfig.title
    card.appendChild(content);
    card.appendChild(style);
    root.appendChild(card);
    this._config = cardConfig;
  }

  _filterCards(attributes) {
    return Object.entries(attributes).filter(elem => (elem[0] != "friendly_name" && elem[0] != "homebridge_hidden" && elem[0] != "domain" && elem[0] != "repo" && elem[0] != "hidden"));
  }

  set hass(hass) {
    const config = this._config;
    const root = this.shadowRoot;
    const card = root.lastChild;
    this.myhass = hass;
    this.handlers = this.handlers || [];
    let card_content = '';
    card_content += `
      <table>
      <thead><tr><th>Name</th><th>Current</th><th>Available</th></tr></thead>
      <tbody>
    `;
    config.trackers.forEach(tracker => {
      if (hass.states[tracker]) {
        const list = this._filterCards(hass.states[tracker].attributes);
        const domain = hass.states[tracker].attributes.domain;
        const repo = hass.states[tracker].attributes.repo;
        card_content += `
          <tr><td colspan='3' class='separator'>${domain.replace('_', ' ')}:</td></tr>
        `;

        if (list !== undefined && list.length > 0) {
          const updated_content = `
            ${list.map(elem => `
                <tr>
                  <td class='name'><a href="${elem[1].repo?elem[1].repo:'#'}" target='_blank'>${elem[0]}</a></td>
                  <td>${elem[1].local?elem[1].local:'n/a'}</td>
                  <td>
                    ${elem[1].has_update?`
                    <a href="${elem[1].change_log?elem[1].change_log:'#'}" target='_blank'>${elem[1].remote?elem[1].remote:'n/a'}</a>
                    `:(elem[1].remote?elem[1].remote:'n/a')}
                    </td>
                </tr>
            `).join('')}
          `;
          card_content += updated_content;
        }
        // attach handlers only once
        if (!this.handlers['custom_updater']) {
          card.querySelector('#update').addEventListener('click', event => {
            this.myhass.callService('custom_updater', 'update_all', {});
          });
          card.querySelector('#check').addEventListener('click', event => {
            this.myhass.callService('custom_updater', 'check_all', {});
          });
          this.handlers['custom_updater'] = true;
        }
        root.lastChild.hass = hass;
      }
    });
    card_content += `</tbody></table>`;
    root.getElementById('content').innerHTML = card_content;

  }
  getCardSize() {
    return 1;
  }
}
customElements.define('tracker-card', TrackerCard);