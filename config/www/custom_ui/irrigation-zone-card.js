class IrrigationZoneCard extends HTMLElement {

  set hass(hass) {
    if (!this.content) {
      const card = document.createElement('ha-card');
      const link = document.createElement('link');
      link.type = 'text/css';
      link.rel = 'stylesheet';
      link.href = '/local/custom_ui/irrigation-zone/irrigation-zone-card.css';
      card.appendChild(link);
      this.content = document.createElement('div');
      this.content.className = 'card';
      card.appendChild(this.content);
      this.appendChild(card);
    }

    const zone_title = this._config.zone_title;
    const next_water = new Date(hass.states[this._config.next_water].state);
    const last_water = new Date(hass.states[this._config.last_water].state);
    const zone_status = hass.states[this._config.zone_status].state;
    const moisture_level = hass.states[this._config.moisture_level].state;
    const temperature = hass.states[this._config.temperature].state;
    const light_level = hass.states[this._config.light_level].state;

    var day_format = { weekday: 'long', month: 'long', day: 'numeric' };
    var time_format = {hour12: "false", hour: "2-digit", minute: "2-digit"};
    var next_water_day = next_water.toLocaleDateString([], day_format);
    var next_water_time = next_water.toLocaleTimeString([], time_format);
    var last_water_day = last_water.toLocaleDateString([], day_format);
    var last_water_time = last_water.toLocaleTimeString([], time_format);

    //const cardtitle = hass.states[this.config.card_title].state;

    this.content.innerHTML = `
      <!-- Main Container -->
      <div class="container" style="background: none, url(/local/custom_ui/irrigation-zone/seedlings.jpg) no-repeat; background-size: contain;"> 
        <!-- Zone Title Section -->
        <section class="irrigation_title">
          <h2 class="irrigation_header">${zone_title}</h2>
        </section>
        <!-- Zone Schedule Gallery Section -->
        <div class="schedule">
          <div class="zone_time">
            <h1 class="time_title">Next Watering Time</h1>
            <h4>${next_water_day}</h4>
            <h4>${next_water_time}</h4>
          </div>
          <div class="zone_time" style="margin-right: 0px;">
            <h1 class="time_title">Last Watering Time</h1>
            <h4>${last_water_day}</h4>
            <h4>${last_water_time}</h4>
          </div>
        </div>
        <div class="states">
          <div class="attribute">
            <h1 class="state_title">Status</h1>
            <h4>${zone_status}</h4>
          </div>
          <div class="attribute">
            <h1 class="state_title">Water Level</h1>
            <h4>${moisture_level}%</h4>
          </div>
          <div class="attribute">
            <h1 class="state_title">Temperature</h1>
            <h4>${temperature}°C</h4>
          </div>
          <div class="attribute">
            <h1 class="state_title">Light Level</h1>
            <h4>${light_level}lx</h4>
          </div>
          <div class="attribute" style="margin-right: 0px;">
            <h1 class="state_title">Settings</h1>
            <h4>COG</h4>
          </div>
        </div>
      </div>`;

  }

  setConfig(config) {
    this._config = config;
    //const cardtitle = config.title;
//    const next_schedule = cardConfig.entity_next_schedule;
    
//    if (!config.entity_next_schedule] ||
//      !config.entity_last_run ||
//      !config.entity_current_status ||
//      !config.entity_manual_activation ||
//      !config.entity_moisture_level ||
//      !config.entity_light_level ||
//      !config.entity_temperature ||
//      !config.entity_currentstate ||
//      !config.entity_zonetitle) {
//      throw new Error('Please define entities');
//    }
//    this.config = config;
  }

  // @TODO: This requires more intelligent logic
  getCardSize() {
    return 3;
  }
}

customElements.define('irrigation-zone-card', IrrigationZoneCard);