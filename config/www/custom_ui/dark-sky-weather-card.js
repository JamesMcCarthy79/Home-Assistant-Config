// #####
// ##### Get the LitElement and HTML classes from an already defined HA Lovelace class
// #####
var LitElement = LitElement || Object.getPrototypeOf(customElements.get("home-assistant-main"));
var html = LitElement.prototype.html;

// #####
// ##### Custom Card Definition begins
// #####

class DarkSkyWeatherCard extends LitElement {

// #####
// ##### Define Render Template
// #####

  render() {
//  Handle Configuration Flags 
//    var icons = this.config.static_icons ? "static" : "animated";
    var currentText = this.config.entity_current_text ? html`<span class="currentText" id="current-text">${this._hass.states[this.config.entity_current_text].state}</span>` : ``;
    var apparentTemp = this.config.entity_apparent_temp ? html`<span class="apparent">${this.localeText.feelsLike} <span id="apparent-text">${this.current.apparent}</span> ${this.getUOM("temperature")}</span>` : ``;
    var summary = this.config.entity_daily_summary ? html`<br><span class="unit" id="daily-summary-text">${this._hass.states[this.config.entity_daily_summary].state}</span></br>` : ``;
    var separator = this.config.show_separator ? html`<hr class=line>` : ``;
    
    
    
// Build HTML    
    return html`
      <style>
      ${this.style()}
      </style>
      <ha-card class = "card">  
        <span class="icon bigger" id="icon-bigger" style="background: none, url(/local/icons/weather_icons/${this.config.static_icons ? "static" : "animated"}/${this.weatherIcons[this.current.conditions]}.svg) no-repeat; background-size: contain;">${this.current.conditions}</span>
        <span class="temp" id="temperature-text">${this.current.temperature}</span><span class="tempc">${this.getUOM('temperature')}</span>
        ${currentText}
        ${apparentTemp}
        ${separator}
        <span>
          <ul class="variations">
            <li>
              ${this.getSlot().l1} 
              ${this.getSlot().l2}
              ${this.getSlot().l3}
              ${this.getSlot().l4}
            </li>
            <li>
              ${this.getSlot().r1}
              ${this.getSlot().r2}
              ${this.getSlot().r3}
              ${this.getSlot().r4}
            </li>
          </ul>
        </span>
            <div class="forecast clear">
              ${this.forecast.map(daily => html`
                <div class="day fcasttooltip">
                  <span class="dayname" id="fcast-dayName-${daily.dayIndex}">${(daily.date).toLocaleDateString(this.config.locale,{weekday: 'short'})}</span>
                  <br><i class="icon" id="fcast-icon-${daily.dayIndex}" style="background: none, url(/local/icons/weather_icons/${this.config.static_icons ? "static" : "animated"}/${this.weatherIcons[this._hass.states[daily.condition].state]}.svg) no-repeat; background-size: contain;"></i>
                  ${this.config.old_daily_format ? html`<br><span class="highTemp" id="fcast-high-${daily.dayIndex}">${Math.round(this._hass.states[daily.temphigh].state)}${this.getUOM("temperature")}</span>
                                                        <br><span class="lowTemp" id="fcast-low-${daily.dayIndex}">${Math.round(this._hass.states[daily.templow].state)}${this.getUOM("temperature")}</span>` : 
                                                   html`<br><span class="lowTemp" id="fcast-low-${daily.dayIndex}">${Math.round(this._hass.states[daily.templow].state)}</span> / <span class="highTemp" id="fcast-high-${daily.dayIndex}">${Math.round(this._hass.states[daily.temphigh].state)}${this.getUOM("temperature")}</span>`}
                  ${this.config.entity_pop_1 && this.config.entity_pop_2 && this.config.entity_pop_3 && this.config.entity_pop_4 && this.config.entity_pop_5 ? html`<br><span class="pop" id="fcast-pop-${daily.dayIndex}">${Math.round(this._hass.states[daily.pop].state)} %</span>` : ``}
                  <div class="fcasttooltiptext" id="fcast-summary-${daily.dayIndex}">${ this.config.tooltips ? this._hass.states[daily.summary].state : ""}</div>
                </div>`)}
              </div>
        ${summary}
      </ha-card>
    `;
  }


// #####
// ##### slots - returns the value to be displyed in a specific current condition slot
// #####
  
  getSlot() {
    return {
      'r1' : this.slotValue('r1',this.config.slot_r1),
      'r2' : this.slotValue('r2',this.config.slot_r2),
      'r3' : this.slotValue('r3',this.config.slot_r3),
      'r4' : this.slotValue('r4',this.config.slot_r4),
      'l1' : this.slotValue('l1',this.config.slot_l1),
      'l2' : this.slotValue('l2',this.config.slot_l2),
      'l3' : this.slotValue('l3',this.config.slot_l3),
      'l4' : this.slotValue('l4',this.config.slot_l4),
    }
  }

// #####
// ##### slots - calculates the specific slot value
// #####

  slotValue(slot,value){
    var sunNext = this.config.alt_sun_next ? html`<li><span id="alt-sun-next">${this._hass.states[this.config.alt_sun_next].state}</span></li>` : this.config.entity_sun ? this.sunSet.next : "";
    var sunFollowing = this.config.alt_sun_following ? html`<li><span id="alt-sun-following">${this._hass.states[this.config.alt_sun_following].state}</span></li>` : this.config.entity_sun ? this.sunSet.following : "";
    var daytimeHigh = this.config.alt_daytime_high ? html`<li><span class="ha-icon"><ha-icon icon="mdi:thermometer"></ha-icon></span><span id="alt-daytime-high">${this._hass.states[this.config.alt_daytime_high].state}</span></li>` : this.config.entity_daytime_high ? html`<li><span class="ha-icon"><ha-icon icon="mdi:thermometer"></ha-icon></span>${this.localeText.maxToday} <span id="daytime-high-text">${Math.round(this._hass.states[this.config.entity_daytime_high].state)}</span><span> ${this.getUOM('temperature')}</span></li>` : ``;
    var intensity = this.config.entity_pop_intensity ? html`<span id="intensity-text"> - ${this._hass.states[this.config.entity_pop_intensity].state}</span><span class="unit"> ${this.getUOM('intensity')}</span>` : ``;
    var pop = this.config.alt_pop ? html`<li><span class="ha-icon"><ha-icon icon="mdi:weather-rainy"></ha-icon></span><span id="alt-pop">${this._hass.states[this.config.alt_pop].state}</span></li>` : this.config.entity_pop ? html`<li><span class="ha-icon"><ha-icon icon="mdi:weather-rainy"></ha-icon></span><span id="pop-text">${Math.round(this._hass.states[this.config.entity_pop].state)}</span> %<span id="pop-intensity-text">${intensity}</span></li>` : ``;
    var visibility = this.config.alt_visibility ? html`<li><span class="ha-icon"><ha-icon icon="mdi:weather-fog"></ha-icon></span><span id="alt-visibility">${this._hass.states[this.config.alt_visibility].state}</span></li>` : this.config.entity_visibility ? html`<li><span class="ha-icon"><ha-icon icon="mdi:weather-fog"></ha-icon></span><span id="visibility-text">${this.current.visibility}</span><span class="unit"> ${this.getUOM('length')}</span></li>` : ``;
    var wind = this.config.alt_wind ? html`<li><span class="ha-icon"><ha-icon icon="mdi:weather-windy"></ha-icon></span><span id="alt-wind">${this._hass.states[this.config.alt_wind].state}</span></li>` : this.config.entity_wind_bearing && this.config.entity_wind_speed ? html`<li><span class="ha-icon"><ha-icon icon="mdi:weather-windy"></ha-icon></span><span id="beaufort-text">${this.current.beaufort}</span><span id="wind-bearing-text">${this.current.windBearing}</span><span id="wind-speed-text"> ${this.current.windSpeed}</span><span class="unit"> ${this.getUOM('length')}/h</span></li>` : ``;
    var humidity = this.config.alt_humidity ? html`<li><span class="ha-icon"><ha-icon icon="mdi:water-percent"></ha-icon></span><span id="alt-humidity">${this._hass.states[this.config.alt_humidity].state}</span></li>` : this.config.entity_humidity ? html`<li><span class="ha-icon"><ha-icon icon="mdi:water-percent"></ha-icon></span><span id="humidity-text">${this.current.humidity}</span><span class="unit"> %</span></li>` : ``;
    var pressure = this.config.alt_pressure ? html`<li><span class="ha-icon"><ha-icon icon="mdi:gauge"></ha-icon></span><span id="alt-pressure">${this._hass.states[this.config.alt_pressure].state}</span></li>` : this.config.entity_pressure ? html`<li><span class="ha-icon"><ha-icon icon="mdi:gauge"></ha-icon></span><span id="pressure-text">${this.current.pressure}</span><span class="unit"> ${this.getUOM('air_pressure')}</span></li>` : ``;

    
    switch (value){
      case 'pop': return pop;
      case 'humidity': return humidity;
      case 'pressure': return pressure;
      case 'sun_following': return sunFollowing;
      case 'daytime_high': return daytimeHigh;
      case 'wind': return wind;
      case 'visibility': return visibility;
      case 'sun_next': return sunNext;
      case 'empty': return html`&nbsp;`;
      case 'remove': return ``;
    }
    
    // If no value can be matched pass back a default for the slot
    switch (slot){
      case 'l1': return daytimeHigh;
      case 'l2': return wind;
      case 'l3': return visibility;
      case 'l4': return sunNext;
      case 'r1': return pop;
      case 'r2': return humidity;
      case 'r3': return pressure;
      case 'r4': return sunFollowing;
    }
  }
  
  
// #####
// ##### windDirections - returns set of possible wind directions by specified language
// #####

  get windDirections() {
    const windDirections_en = ['N','NNE','NE','ENE','E','ESE','SE','SSE','S','SSW','SW','WSW','W','WNW','NW','NNW','N'];
    const windDirections_fr = ['N','NNE','NE','ENE','E','ESE','SE','SSE','S','SSO','SO','OSO','O','ONO','NO','NNO','N'];
    const windDirections_de = ['N','NNO','NO','ONO','O','OSO','SO','SSO','S','SSW','SW','WSW','W','WNW','NW','NNW','N'];
    const windDirections_nl = ['N','NNO','NO','ONO','O','OZO','ZO','ZZO','Z','ZZW','ZW','WZW','W','WNW','NW','NNW','N'];
    const windDirections_he = ['צפון','צ-צ-מז','צפון מזרח','מז-צ-מז','מזרח','מז-ד-מז','דרום מזרח','ד-ד-מז','דרום','ד-ד-מע','דרום מערב','מע-ד-מע','מערב','מע-צ-מע','צפון מערב','צ-צ-מע','צפון'];
    const windDirections_da = ['N','NNØ','NØ','ØNØ','Ø','ØSØ','SØ','SSØ','S','SSV','SV','VSV','V','VNV','NV','NNV','N'];
    
    switch (this.config.locale) {
      case "it" :
      case "fr" :
        return windDirections_fr;
      case "de" :
        return windDirections_de;
      case "nl" :
        return windDirections_nl;
      case "he" :
        return windDirections_he;
      case "da" :
        return windDirections_da;
      default :
        return windDirections_en;
    }
  }

// #####
// ##### feelsLikeText returns set of possible "Feels Like" text by specified language
// #####

  get localeText() {
    switch (this.config.locale) {
      case "it" :
        return {
          feelsLike: "Percepito",
          maxToday: "Max oggi:",
        }
      case "fr" :
        return {
          feelsLike: "Se sent comme",
          maxToday: "Max aujourd'hui:",
        }
      case "de" :
        return {
          feelsLike: "Gefühlt",
          maxToday: "Max heute:",
        }
      case "nl" :
        return {
          feelsLike: "Voelt als",
          maxToday: "Max vandaag:",
        }
      case "pl" :
        return {
          feelsLike: "Odczuwalne",
          maxToday: "Najwyższa dziś:",
        }
      case "he" :
        return {
          feelsLike: "מרגיש כמו:",
          maxToday: "מקסימלי היום:",
        }
      case "da" :
        return {
          feelsLike: "Føles som",
          maxToday: "Højeste i dag"
        }
      default :
        return {
          feelsLike: "Feels like",
          maxToday: "Today's High",
        }
    }
  }
  
// #####
// ##### dayOrNight : returns day or night depending on the position of the sun.
// #####

  get dayOrNight() {
    const transformDayNight = { "below_horizon": "night", "above_horizon": "day", };
    return this.config.entity_sun ? transformDayNight[this._hass.states[this.config.entity_sun].state] : 'day';
  }


// #####
// ##### weatherIcons: returns icon names based on current conditions text
// #####

  get weatherIcons() {
    return {
      'clear-day': 'day',
      'clear-night': 'night',
      'rain': 'rainy-5',
      'snow': 'snowy-6',
      'sleet': 'rainy-6',
      'wind': 'cloudy',
      'fog': 'cloudy',
      'cloudy': 'cloudy',
      'partly-cloudy-day': 'cloudy-day-3',
      'partly-cloudy-night': 'cloudy-night-3',
      'hail': 'rainy-7',
      'lightning': 'thunder',
      'thunderstorm': 'thunder',
      'windy-variant': html`cloudy-${this.dayOrNight}-3`,
      'exceptional': '!!',
    }
  }


// #####
// ##### forecast : returns forcasted weather information for the next 5 days
// #####

  get forecast() {
    var forecastDate1 = new Date();
    forecastDate1.setDate(forecastDate1.getDate()+1);
    var forecastDate2 = new Date();
    forecastDate2.setDate(forecastDate2.getDate()+2);
    var forecastDate3 = new Date();
    forecastDate3.setDate(forecastDate3.getDate()+3);
    var forecastDate4 = new Date();
    forecastDate4.setDate(forecastDate4.getDate()+4);
    var forecastDate5 = new Date();
    forecastDate5.setDate(forecastDate5.getDate()+5);
    

    const forecast1 = { date: forecastDate1,
                      dayIndex: '1',
  	                  condition: this.config.entity_forecast_icon_1,
  										temphigh: this.config.entity_forecast_high_temp_1,
  										templow:  this.config.entity_forecast_low_temp_1,
  										pop: this.config.entity_pop_1,
  										summary: this.config.entity_summary_1, };
    const forecast2 = { date: forecastDate2,
                      dayIndex: '2',
  	                  condition: this.config.entity_forecast_icon_2,
  										temphigh: this.config.entity_forecast_high_temp_2,
  										templow:  this.config.entity_forecast_low_temp_2,
  										pop: this.config.entity_pop_2,
  										summary: this.config.entity_summary_2,  };
    const forecast3 = { date: forecastDate3,
                      dayIndex: '3',
  	                  condition: this.config.entity_forecast_icon_3,
  										temphigh: this.config.entity_forecast_high_temp_3,
  										templow:  this.config.entity_forecast_low_temp_3,
  										pop: this.config.entity_pop_3,
  										summary: this.config.entity_summary_3, };
    const forecast4 = { date: forecastDate4,
                      dayIndex: '4',
  	                  condition: this.config.entity_forecast_icon_4,
  										temphigh: this.config.entity_forecast_high_temp_4,
  										templow:  this.config.entity_forecast_low_temp_4,
  										pop: this.config.entity_pop_4,
  										summary: this.config.entity_summary_4, };
    const forecast5 = { date: forecastDate5,
                      dayIndex: '5',
  	                  condition: this.config.entity_forecast_icon_5,
  										temphigh: this.config.entity_forecast_high_temp_5,
  										templow:  this.config.entity_forecast_low_temp_5,
  										pop: this.config.entity_pop_5,
  										summary: this.config.entity_summary_5, };

	  return [forecast1, forecast2, forecast3, forecast4, forecast5];
  }


// #####
// ##### current : Returns current weather information
// #####

  get current() {
    var conditions = this._hass.states[this.config.entity_current_conditions].state;
    var humidity = this.config.entity_humidity ? this._hass.states[this.config.entity_humidity].state : 0;
    var pressure = this.config.entity_pressure ? Math.round(this._hass.states[this.config.entity_pressure].state) : 0;
    var temperature = Math.round(this._hass.states[this.config.entity_temperature].state);
    var visibility = this.config.entity_visibility ? this._hass.states[this.config.entity_visibility].state : 0;
    var windBearing = this.config.entity_wind_bearing ? isNaN(this._hass.states[this.config.entity_wind_bearing].state) ? this._hass.states[this.config.entity_wind_bearing].state : this.windDirections[(Math.round((this._hass.states[this.config.entity_wind_bearing].state / 360) * 16))] : 0;
    var windSpeed = this.config.entity_wind_speed ? Math.round(this._hass.states[this.config.entity_wind_speed].state) : 0;
    var apparent = this.config.entity_apparent_temp ? Math.round(this._hass.states[this.config.entity_apparent_temp].state) : 0;
    var beaufort = this.config.show_beaufort ? html`Bft: ${this.beaufortWind} - ` : ``;
    
    return {
      'conditions': conditions,
      'humidity': humidity,
      'pressure': pressure,
      'temperature': temperature,
      'visibility': visibility,
      'windBearing': windBearing,
      'windSpeed': windSpeed,
      'apparent' : apparent,
      'beaufort' : beaufort,
    }
  }

// #####
// ##### sunSetAndRise: returns set and rise information
// #####

get sunSet() {
    var nextSunSet ;
    var nextSunRise;
    if (this.config.time_format) {
      nextSunSet = new Date(this._hass.states[this.config.entity_sun].attributes.next_setting).toLocaleTimeString(this.config.locale, {hour: '2-digit', minute:'2-digit',hour12: this.is12Hour});
      nextSunRise = new Date(this._hass.states[this.config.entity_sun].attributes.next_rising).toLocaleTimeString(this.config.locale, {hour: '2-digit', minute:'2-digit', hour12: this.is12Hour});
    }
    else {
      nextSunSet = new Date(this._hass.states[this.config.entity_sun].attributes.next_setting).toLocaleTimeString(this.config.locale, {hour: '2-digit', minute:'2-digit'});
      nextSunRise = new Date(this._hass.states[this.config.entity_sun].attributes.next_rising).toLocaleTimeString(this.config.locale, {hour: '2-digit', minute:'2-digit'});
    }
    var nextDate = new Date();
    nextDate.setDate(nextDate.getDate() + 1);
    if (this._hass.states[this.config.entity_sun].state == "above_horizon" ) {
      nextSunRise = nextDate.toLocaleDateString(this.config.locale,{weekday: 'short'}) + " " + nextSunRise;
      return {
      'next': html`<li><span class="ha-icon"><ha-icon icon="mdi:weather-sunset-down"></ha-icon></span><span id="sun-next-text">${nextSunSet}</span></li>`,
      'following': html`<li><span class="ha-icon"><ha-icon icon="mdi:weather-sunset-up"></ha-icon></span><span id="sun-following-text">${nextSunRise}</span></li>`,
      'nextText': nextSunSet,
      'followingText': nextSunRise,
      };
    } else {
      if (new Date().getDate() != new Date(this._hass.states[this.config.entity_sun].attributes.next_rising).getDate()) {
        nextSunRise = nextDate.toLocaleDateString(this.config.locale,{weekday: 'short'}) + " " + nextSunRise;
        nextSunSet = nextDate.toLocaleDateString(this.config.locale,{weekday: 'short'}) + " " + nextSunSet;
      } 
      return {
      'next': html`<li><span class="ha-icon"><ha-icon icon="mdi:weather-sunset-up"></ha-icon></span><span id="sun-next-text">${nextSunRise}</span></li>`,
      'following': html`<li><span class="ha-icon"><ha-icon icon="mdi:weather-sunset-down"></ha-icon></span><span id="sun-following-text">${nextSunSet}</span></li>`,
      'nextText': nextSunRise,
      'followingText': nextSunSet,
      };
    }
}


// #####
// ##### beaufortWind - returns the wind speed on th beaufort scale
// #####

get beaufortWind() { 
  if (this.config.entity_wind_speed) {
    switch (this._hass.states[this.config.entity_wind_speed].attributes.unit_of_measurement) {
      case 'mph':
        if (this._hass.states[this.config.entity_wind_speed].state >= 73) return 12;
        if (this._hass.states[this.config.entity_wind_speed].state >= 64) return 11;
        if (this._hass.states[this.config.entity_wind_speed].state >= 55) return 10;
        if (this._hass.states[this.config.entity_wind_speed].state >= 47) return 9;
        if (this._hass.states[this.config.entity_wind_speed].state >= 39) return 8;
        if (this._hass.states[this.config.entity_wind_speed].state >= 31) return 7;
        if (this._hass.states[this.config.entity_wind_speed].state >= 25) return 6;
        if (this._hass.states[this.config.entity_wind_speed].state >= 18) return 5;
        if (this._hass.states[this.config.entity_wind_speed].state >= 13) return 4;
        if (this._hass.states[this.config.entity_wind_speed].state >= 8) return 3;
        if (this._hass.states[this.config.entity_wind_speed].state >=3) return 2;
        if (this._hass.states[this.config.entity_wind_speed].state >= 1) return 1;
      default: // Assume m/s
        if ((this._hass.states[this.config.entity_wind_speed].state * 3.6) >= 118) return 12;
        if ((this._hass.states[this.config.entity_wind_speed].state * 3.6) >= 103) return 11;
        if ((this._hass.states[this.config.entity_wind_speed].state * 3.6) >= 89) return 10;
        if ((this._hass.states[this.config.entity_wind_speed].state * 3.6) >= 75) return 9;
        if ((this._hass.states[this.config.entity_wind_speed].state * 3.6) >= 62) return 8;
        if ((this._hass.states[this.config.entity_wind_speed].state * 3.6) >= 50) return 7;
        if ((this._hass.states[this.config.entity_wind_speed].state * 3.6) >= 39) return 6;
        if ((this._hass.states[this.config.entity_wind_speed].state * 3.6) >= 29) return 5;
        if ((this._hass.states[this.config.entity_wind_speed].state * 3.6) >= 20) return 4;
        if ((this._hass.states[this.config.entity_wind_speed].state * 3.6) >= 12) return 3;
        if ((this._hass.states[this.config.entity_wind_speed].state * 3.6) >=6) return 2;
        if ((this._hass.states[this.config.entity_wind_speed].state * 3.6) >= 1) return 1;
    }
  }
  return 0;
}


// #####
// ##### is12Hour - returns true if 12 hour clock or false if 24
// #####

get is12Hour() {
  var hourFormat= this.config.time_format ? this.config.time_format : 12
  switch (hourFormat) {
    case 24:
      return false;
    default:
      return true;
  }
}


// #####
// ##### style: returns the CSS style classes for the card
// ####

style() {
  
  // Get config flags or set defaults if not configured
  var tooltipBGColor = this.config.tooltip_bg_color || "rgb( 75,155,239)";
  var tooltipFGColor = this.config.tooltip_fg_color || "#fff";
  var tooltipBorderColor = this.config.tooltip_border_color || "rgb(255,161,0)";
  var tooltipBorderWidth = this.config.tooltip_border_width || "1";
  var tooltipCaretSize = this.config.tooltip_caret_size || "5";
  var tooltipWidth = this.config.tooltip_width || "110";
  var tooltipLeftOffset = this.config.tooltip_left_offset || "-12";
  var tooltipVisible = this.config.tooltips ? "visible" : "hidden";
  var tempTopMargin = this.config.temp_top_margin || "-0.3em";
  var tempFontWeight = this.config.temp_font_weight || "300";
  var tempFontSize = this.config.temp_font_size || "4em";
  var tempRightPos = this.config.temp_right_pos || "0.85em";
  var tempUOMTopMargin = this.config.temp_uom_top_margin || "-9px";
  var tempUOMRightMargin = this.config.temp_uom_right_margin || "7px";
  var apparentTopMargin = this.config.apparent_top_margin || "45px";
  var apparentRightPos =  this.config.apparent_right_pos || "1em";
  var apparentRightMargin = this.config.apparent_right_margin || "1em";
  var currentTextTopMargin = this.config.current_text_top_margin || "39px";
  var currentTextLeftPos = this.config.current_text_left_pos || "5em";
  var currentTextFontSize = this.config.current_text_font_size || "1.5em";
  var largeIconTopMargin = this.config.large_icon_top_margin || "-3.5em";
  var largeIconLeftPos = this.config.large_icon_left_pos || "0em";
  var currentDataTopMargin = this.config.current_data_top_margin ? this.config.current_data_top_margin : this.config.show_separator ? "1em" : "7em";
  var separatorTopMargin = this.config.separator_top_margin || "6em";
  
  return html`
        .clear {
        clear: both;
      }
      .card {
        margin: auto;
        padding-top: 2em;
        padding-bottom: 1em;
        padding-left: 1em;
        padding-right: 1em;
        position: relative;
      }
      .ha-icon {
        height: 18px;
        margin-right: 5px;
        color: var(--paper-item-icon-color);
      }
      .line {
        margin-top: ${separatorTopMargin};
        margin-left: 1em;
        margin-right: 1em;
      }
      
      .temp {
        font-weight: ${tempFontWeight};
        font-size: ${tempFontSize};
        color: var(--primary-text-color);
        position: absolute;
        right: ${tempRightPos};
        margin-top: ${tempTopMargin};
      }
      .tempc {
        font-weight: ${tempFontWeight};
        font-size: 1.5em;
        vertical-align: super;
        color: var(--primary-text-color);
        position: absolute;
        right: 1em;
        margin-top: ${tempUOMTopMargin};
        margin-right: ${tempUOMRightMargin};
      }
      .apparent {
        color: var(--primary-text-color);
        position: absolute;
        right: ${apparentRightPos};
        margin-top: ${apparentTopMargin};
        margin-right: ${apparentRightMargin};
      }
      .currentText {
        font-size: ${currentTextFontSize};
        color: var(--secondary-text-color);
        position: absolute;
        left: ${currentTextLeftPos};
        margin-top: ${currentTextTopMargin};
      }
      
      .pop {
        font-weight: 400;
        color: var(--primary-text-color);
      }
      .variations {
        display: flex;
        flex-flow: row wrap;
        justify-content: space-between;
        font-weight: 300;
        color: var(--primary-text-color);
        list-style: none;
        padding: 0.2em;
        margin-top: ${currentDataTopMargin};
      }
      .unit {
        font-size: 0.8em;
      }
      .forecast {
        width: 100%;
        margin: 0 auto;
        height: 9em;
      }
      .day {
        display: block;
        width: 20%;
        float: left;
        text-align: center;
        color: var(--primary-text-color);
        border-right: .1em solid #d9d9d9;
        line-height: 1.5;
        box-sizing: border-box;
        margin-top: 1em;
      }
      .dayname {
        text-transform: uppercase;
      }
      .forecast .day:first-child {
        margin-left: 20;
      }
      .forecast .day:nth-last-child(1) {
        border-right: none;
        margin-right: 0;
      }
      .highTemp {
        font-weight: bold;
      }
      .lowTemp {
        color: var(--secondary-text-color);
      }
      .icon.bigger {
        width: 10em;
        height: 10em;
        margin-top: ${largeIconTopMargin};
        position: absolute;
        left: ${largeIconLeftPos};
      }
      .icon {
        width: 50px;
        height: 50px;
        margin-right: 5px;
        display: inline-block;
        vertical-align: middle;
        background-size: contain;
        background-position: center center;
        background-repeat: no-repeat;
        text-indent: -9999px;
      }
      .weather {
        font-weight: 300;
        font-size: 1.5em;
        color: var(--primary-text-color);
        text-align: left;
        position: absolute;
        top: -0.5em;
        left: 6em;
        word-wrap: break-word;
        width: 30%;
      }
  
      .fcasttooltip {
        position: relative;
        display: inline-block;
      }
      .fcasttooltip .fcasttooltiptext {
        visibility: hidden;
        width: ${tooltipWidth}px;
        background-color: ${tooltipBGColor};
        color: ${tooltipFGColor};
        text-align: center; 
        border-radius: 6px;
        border-style: solid;
        border-color: ${tooltipBorderColor};
        border-width: ${tooltipBorderWidth}px;
        padding: 5px 0;
        /* Position the tooltip */
        position: absolute;
        z-index: 1;
        bottom: 50%;
        left: 0%; 
        margin-left: ${tooltipLeftOffset}px;
      }
      .fcasttooltip .fcasttooltiptext:after {
        content: "";
        position: absolute;
        top: 100%;
        left: 50%;
        margin-left: -${tooltipCaretSize}px;
        border-width: ${tooltipCaretSize}px;
        border-style: solid;
        border-color: ${tooltipBorderColor} transparent transparent transparent;
      }
      .fcasttooltip:hover .fcasttooltiptext {
        visibility: ${tooltipVisible};
      }
      `
}

// #####
// ##### getUOM: gets UOM for specified measure in either metric or imperial
// #####

  getUOM(measure) {
    
    const lengthUnit = this._hass.config.unit_system.length;
    
    switch (measure) {
      case 'air_pressure':
        return lengthUnit === 'km' ? 'hPa' : 'mbar';
      case 'length':
        return lengthUnit;
      case 'precipitation':
        return lengthUnit === 'km' ? 'mm' : 'in';
      case 'intensity':
        return lengthUnit === 'km' ? 'mm/h' : 'in/h'
      default:
        return this._hass.config.unit_system[measure] || '';
    }
  }

// #####
// ##### Assign the external hass object to an internal class var.
// ##### This is called everytime a state change occurs in HA
// #####

  set hass(hass) {
    
    var interval = this.config.refresh_interval || 30;
    var doRefresh = false;
    
    // Make sure hass is assigned first time.
    if (!this._initialized) {
      this._initialized= true;
      this._lasRefresh = new Date();
      doRefresh = true;
    }
    
    var now = new Date();
    
    // Check if refresh interval has been exceeded and refresh if necessary
    if (Math.round((now - this._lastRefresh)/1000) > interval ) { doRefresh = true; } 

    if (doRefresh) {
      this._lastRefresh = new Date();
      this._hass = hass;
      this.updateValues();
    }
  }

  
// #####
// updateValues - Updates card values as changes happen in the hass object
// #####

  updateValues() {
    const root = this.shadowRoot;
    if (root.childElementCount > 0) {

// Current Conditions
      root.getElementById("temperature-text").textContent = `${this.current.temperature}`;
      root.getElementById("icon-bigger").textContent = `${this.current.conditions}`;
      root.getElementById("icon-bigger").style.backgroundImage = `none, url(/local/icons/weather_icons/${this.config.static_icons ? "static" : "animated"}/${this.weatherIcons[this.current.conditions]}.svg)`;

// Forecast blocks
      this.forecast.forEach((daily) => {
        root.getElementById("fcast-dayName-" + daily.dayIndex).textContent = `${(daily.date).toLocaleDateString(this.config.locale,{weekday: 'short'})}`;
        root.getElementById("fcast-icon-" + daily.dayIndex).style.backgroundImage = `none, url(/local/icons/weather_icons/${this.config.static_icons ? "static" : "animated"}/${this.weatherIcons[this._hass.states[daily.condition].state]}.svg`;
        root.getElementById("fcast-high-" + daily.dayIndex).textContent = `${Math.round(this._hass.states[daily.temphigh].state)}${this.getUOM("temperature")}`;
        root.getElementById("fcast-low-" + daily.dayIndex).textContent = `${Math.round(this._hass.states[daily.templow].state)}${this.config.old_daily_format ? this.getUOM("temperature") : ""}`;
        if (this.config.entity_pop_1 && this.config.entity_pop_2 && this.config.entity_pop_3 && this.config.entity_pop_4 && this.config.entity_pop_5) { root.getElementById("fcast-pop-" + daily.dayIndex).textContent = `${Math.round(this._hass.states[daily.pop].state)} %` }
        root.getElementById("fcast-summary-" + daily.dayIndex).textContent = `${this._hass.states[daily.summary].state}`;
     });
      
// Optional Entities    
      if (this.config.entity_current_text) { root.getElementById("current-text").textContent = `${this._hass.states[this.config.entity_current_text].state}` }
      if (this.config.entity_apparent_temp) { root.getElementById("apparent-text").textContent = `${this.current.apparent}` }
      if (this.config.entity_pressure && !this.config.alt_pressure) { root.getElementById("pressure-text").textContent = `${this.current.pressure}` }
      if (this.config.entity_humidity && !this.config.alt_humidity) { root.getElementById("humidity-text").textContent = `${this.current.humidity}` }
      if (this.config.show_beaufort  && !this.config.alt_wind) { root.getElementById("beaufort-text").textContent =  `Bft: ${this.beaufortWind} - ` }
      if (this.config.entity_wind_bearing  && !this.config.alt_wind) { root.getElementById("wind-bearing-text").textContent = `${this.current.windBearing} ` }
      if (this.config.entity_wind_speed && !this.config.alt_wind) { root.getElementById("wind-speed-text").textContent = `${this.current.windSpeed}` }
      if (this.config.entity_visibility && !this.config.alt_visibility) { root.getElementById("visibility-text").textContent = `${this.current.visibility}` }
      if (this.config.entity_pop && !this.config.alt_pop) { root.getElementById("pop-text").textContent = `${Math.round(this._hass.states[this.config.entity_pop].state)}` }
      if (this.config.entity_pop_intensity && !this.config.alt_pop) { root.getElementById("pop-intensity-text").textContent = ` - ${this._hass.states[this.config.entity_pop_intensity].state} ${this.getUOM('intensity')}` }
      if (this.config.entity_daytime_high && !this.config.alt_daytime_high) { root.getElementById("daytime-high-text").textContent = `${Math.round(this._hass.states[this.config.entity_daytime_high].state)}` }
      if (this.config.entity_sun && !this.config.alt_sun_next) { root.getElementById("sun-next-text").textContent = `${this.sunSet.nextText}` }
      if (this.config.entity_sun && !this.config.alt_sun_following) { root.getElementById("sun-following-text").textContent = `${this.sunSet.followingText}` }
      if (this.config.entity_daily_summary) { root.getElementById("daily-summary-text").textContent = `${this._hass.states[this.config.entity_daily_summary].state}` }
      
// Alt Text
      if (this.config.alt_sun_next) { root.getElementById("alt-sun-next").textContent = `${this._hass.states[this.config.alt_sun_next].state}` }
      if (this.config.alt_sun_following) { root.getElementById("alt-sun-following").textContent = `${this._hass.states[this.config.alt_sun_following].state}` }
      if (this.config.alt_pop) { root.getElementById("alt-pop").textContent = `${this._hass.states[this.config.alt_pop].state}` }
      if (this.config.alt_wind) { root.getElementById("alt-wind").textContent = `${this._hass.states[this.config.alt_wind].state}` }
      if (this.config.alt_pressure) { root.getElementById("alt-pressure").textContent = `${this._hass.states[this.config.alt_pressure].state}` }
      if (this.config.alt_humidity) { root.getElementById("alt-humidity").textContent = `${this._hass.states[this.config.alt_humidity].state}` }
      if (this.config.alt_daytime_high) { root.getElementById("alt-daytime-high").textContent = `${this._hass.states[this.config.alt_daytime_high].state}` }
      if (this.config.alt_visibility) { root.getElementById("alt-visibility").textContent = `${this._hass.states[this.config.alt_visibility].state}` }
    }
  }
  
  
// #####
// ##### Assigns the configuration vlaues to an internal class var
// ##### This is called everytime a config change is made
// #####

  setConfig(config) { this.config = config; }


// #####
// ##### Sets the card size so HA knows how to put in columns
// #####

  getCardSize() { return 3 }
  
}

// ##### 
// ##### Register the card as a customElement
// #####
customElements.define('dark-sky-weather-card', DarkSkyWeatherCard);