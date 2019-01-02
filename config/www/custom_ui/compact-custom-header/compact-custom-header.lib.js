// Avoid "already defined" errors when navigating away from Lovelace and back.
if (doc_root == undefined) {
  var app_layout, card, chevron, div_view, doc_root, drawer_layout, edit_mode,
      hui_root, icon, iron_icon, love_lace, main, menu_btn, menu_icon,
      menu_iron_icon, notify_btn, notify_icon, notify_dot, notify_iron_icon,
      options_btn, options_icon, options_iron_icon, pages, panel, proceed,
      raw_config, tabs, tabs_container, tabs_count, toolbar, voice_btn,
      voice_icon, voice_iron_icon;
}
// Try so that if we're not on a lovelace page it won't continue to run.
try {
  // Get the parents of the elements to style.
  doc_root = document.querySelector('home-assistant').shadowRoot;
  main = doc_root.querySelector('home-assistant-main').shadowRoot;
  drawer_layout = main.querySelector('app-drawer-layout');
  pages = drawer_layout.querySelector('partial-panel-resolver').shadowRoot;
  panel = pages.querySelector('[id="panel"]');
  love_lace = panel.querySelector('ha-panel-lovelace').shadowRoot;
  proceed = true;
} catch (e) {
  proceed = false;
  console.log(e);
}
// If parent elements exist proceed.
if (proceed) {
  // Get elements to style.
  hui_root = love_lace.querySelector('hui-root').shadowRoot;
  app_layout = hui_root.querySelector('ha-app-layout');
  div_view = app_layout.querySelector('[id="view"]');
  tabs = hui_root.querySelector('paper-tabs');
  tabs_count = tabs.querySelectorAll('paper-tab');
  tabs_container = tabs.shadowRoot.getElementById('tabsContainer');
  chevron = tabs.shadowRoot.querySelectorAll('[icon^="paper-tabs:chevron"]');
  toolbar = hui_root.querySelectorAll('app-toolbar');

  // Find the card element.
  recursive_walk(app_layout, function(node) {
    card = node.nodeName == 'COMPACT-CUSTOM-HEADER' ? node : null;
  });

  // When exiting raw config editor buttons are hidden.
  raw_config = hui_root.querySelector('ha-menu-button') == null;
  // If multiple toolbars exist & 2nd one is displayed, edit mode is active.
  if (toolbar != null && toolbar.length > 1) {
    edit_mode = toolbar[1].style.cssText != 'display: none;' ? true : false;
  } else {
    edit_mode = false;
  }

  // Card styling.
  let button_style = `
    margin:auto;
    margin-bottom:10px;
    background-color:var(--primary-color);
    color:var(--primary-text-color);
    border-radius:8px;
    display:inline-block;
    border:0;
    font-size:14px;
    width:30%;
    padding:10px 0 10px 0;
    outline:0 !important;
  `;
  let h2_style = `
    margin:auto auto 10px auto;
    padding:20px;
    background-color:var(--primary-color);
  `;
  let svg_style = `
    float:left;
    height:30px;
    padding:15px 5px 15px 15px;
  `;
  let div_style = `
    display: flex;
    justify-content: center;
  `;
  let path = `
    fill="var(--primary-text-color)"
    d="M12,7L17,12H14V16H10V12H7L12,7M19,
    21H5A2,2 0 0,1 3,19V5A2,2 0 0,1 5,
    3H19A2,2 0 0,1 21,5V19A2,2 0 0,1 19,
    21M19,19V5H5V19H19Z"
   `;
  let user_agent = `
    padding:5px;
    border:0;
    resize:none;
    width:100%;
  `;

  // Hide whole column if this card is the only one it contains.
  if (card != null) {
    if (card.parentNode.children.length == 1) {
      card.parentNode.style.cssText = 'display:none';
    } else {
      card.parentNode.style.cssText = '';
    }
    // Create and display card in edit & raw config modes.
    if (edit_mode || raw_config) {
      let ua_text = window.cch_ua_display ? 'Hide' : 'Show';
      let tabs_text = window.cch_tabs_display ? 'Revert' : 'Show';
      card.style.cssText = '';
      card.innerHTML = `
        <svg style="${svg_style}" viewBox="0 0 24 24">
          <path ${path}></path>
        </svg>
        <h2 style="${h2_style}">Compact Custom Header</h2>
        <div style="${div_style}">
          <button id='btn_ua' style="${button_style}"
            onclick="show_user_agent()">
            ${ua_text} user agent</button>
          <button id='btn_tabs' style="${button_style}"
            onclick="show_all_tabs()">
            ${tabs_text} all tabs</button>
          <button style="${button_style}"
            onclick="location.reload(true);">
            Refresh</button>
        </div>
        <div style="${div_style}">
          <textarea style="${user_agent} "id="cch_ua" rows="4" readonly>
          </textarea>
        </div>
      `;
      card.parentNode.style.cssText = `
        background-color:var(--paper-card-background-color);
      `;
      if (!window.cch_ua_display) {
        card.querySelector('[id="cch_ua"]').style.display = 'none';
      }
      card.querySelector('[id="cch_ua"]').innerHTML = navigator.userAgent;
    } else {
      // Hide card outside of edit mode.
      card.style.cssText = 'display:none';
      card.innerHTML = '';
    }
  }
  // Resize to update header.
  window.dispatchEvent(new Event('resize'));

  // Style header and icons.
  if (!window.cch_disable && !raw_config) {
    menu_btn = hui_root.querySelector('ha-menu-button');
    menu_icon = menu_btn.shadowRoot.querySelector('paper-icon-button');
    menu_iron_icon = menu_icon.shadowRoot.querySelector('iron-icon');
    notify_btn = hui_root.querySelector('hui-notifications-button');
    notify_icon = notify_btn.shadowRoot.querySelector('paper-icon-button');
    notify_iron_icon = notify_icon.shadowRoot.querySelector('iron-icon');
    notify_dot = notify_btn.shadowRoot.querySelector('[class="indicator"]');
    voice_btn = hui_root.querySelector('ha-start-voice-button');
    voice_icon = voice_btn.shadowRoot.querySelector('paper-icon-button');
    voice_iron_icon = voice_icon.shadowRoot.querySelector('iron-icon');
    options_btn = hui_root.querySelector('paper-menu-button');
    options_icon = options_btn.querySelector('paper-icon-button');
    options_iron_icon = options_icon.shadowRoot.querySelector('iron-icon');

    if (window.cch_ua_views && !window.cch_tabs_display) {
      // Hide or show tabs.
      for (let i = 0; i < tabs_count.length; i++) {
        if (window.cch_ua_views.indexOf(String(i+1)) > -1) {
          element_style(window.cch_tabs, tabs_count[i], false);
        } else {
          tabs_count[i].style.cssText = 'display:none;';
        }
      }
      // If user agent settings hide first tab, then redirect to new first tab.
      if (!window.cch_tabs_display && window.cch_ua_views[0] > 1 &&
          tabs_count[0].className == 'iron-selected') {
        tabs_count[parseInt(window.cch_ua_views[0]) - 1].click();
      }
    } else {
      for (let i = 0; i < tabs_count.length; i++) {
          element_style(window.cch_tabs, tabs_count[i], false);
        }
    }

    // Remove clock from element if no longer set.
    remove_clock('notification', notify_icon, notify_btn);
    remove_clock('voice', voice_icon, voice_btn);
    remove_clock('options', options_icon, options_btn);
    remove_clock('menu', menu_icon, menu_btn);
  
    // Hide or show buttons.
    element_style(window.cch_menu, menu_btn, true);
    element_style(window.cch_notify, notify_btn, true);
    element_style(window.cch_voice, voice_btn, true);
    element_style(window.cch_options, options_btn, true);

    // Hide scroll arrows on tab bar to save space.
    chevron[0].style.cssText = 'display:none;';
    chevron[1].style.cssText = 'display:none;';
    // Pad bottom for image backgrounds as we're shifted -64px.
    if (window.cch_background_image) {
      div_view.style.paddingBottom = '64px';
    } else {
      div_view.style.paddingBottom = '';
    }
    // Hide header if set to false in config
    if (!window.cch_header) {
      hui_root.querySelector('app-header').style.cssText = 'display:none;';
    }

    // Shift the header up to hide unused portion, but only with multiple tabs.
    // When there is only one tab the header is already collapsed.
    if (tabs_count.length > 1) {
      hui_root.querySelector('app-toolbar').style.cssText = 'margin-top:-64px;';
    }

    // Add width of all visible elements on right side for tabs margin.
    let pad = 20;
    pad += window.cch_notify && window.cch_clock != 'notification' ? 40 : 0;
    pad += window.cch_voice && window.cch_clock != 'voice' ? 40 : 0;
    pad += window.cch_options && window.cch_clock != 'options' ? 56 : 0;
    if (window.cch_clock) {
      pad += window.cch_am_pm && window.ch_clock_format == 12 ? 30 : 0;
      pad += 60;
    }
    tabs.style.cssText = `margin-right:${pad}px;`;

    // Set width of clock based on format options.
    let clock_width = window.cch_clock_format == 12 && window.cch_am_pm ?
      90 : 70;
    // Add margin to the left side if the menu button is a clock.
    if (window.cch_menu && window.cch_clock != 'menu') {
      tabs_container.style.cssText = 'margin-left:60px;';
    } else if (window.cch_menu && window.cch_clock == 'menu') {
      tabs_container.style.cssText = `margin-left:${clock_width + 15}px;`;
    }

    // Strings to compare config to. Avoids errors while typing in edit field.
    let clock_strings = ['notification','voice','options','menu'];

    // Get elements to style for clock choice.
    if (clock_strings.indexOf(window.cch_clock) > -1) {
      if (window.cch_clock == 'notification') {
        icon = notify_icon;
        iron_icon = notify_iron_icon;
        notify_dot.style.cssText = 'top:14.5px;left:-7px';
      } else if (window.cch_clock == 'voice') {
        icon = voice_icon;
        iron_icon = voice_iron_icon;
      } else if (window.cch_clock == 'options') {
        icon = options_icon;
        iron_icon = options_iron_icon;
      } else if (window.cch_clock == 'menu') {
        icon = menu_icon;
        iron_icon = menu_iron_icon;
      }
      // If the clock element doesn't exist yet, create & insert.
      if (window.cch_clock && clock == null) {
        let create_clock = document.createElement('p');
        create_clock.setAttribute('id','cch_clock');
        create_clock.style.cssText = `
          width:${clock_width}px;
          margin-top:2px;
          margin-left:-8px;
        `;
        iron_icon.parentNode.insertBefore(create_clock, iron_icon);
      }
      // Style clock and insert time text.
      var clock = icon.shadowRoot.getElementById('cch_clock');
      if (window.cch_clock && clock != null) {
        let clock_format = {
          'hour12': (window.cch_clock_format != 24),
          'hour': '2-digit',
          'minute': '2-digit'
        };
        let date = new Date();
        date = date.toLocaleTimeString([], clock_format);
        if (!window.cch_am_pm && window.ch_clock_format == 12) {
          clock.innerHTML = date.slice(0, -3);
        } else {
          clock.innerHTML = date;
        }
        icon.style.cssText = `
          margin-right:-5px;
          width:${clock_width}px;
          text-align: center;
        `;
        iron_icon.style.cssText = 'display:none;';
        window.dispatchEvent(new Event('resize'));
      }
    }
  }

  window.dispatchEvent(new Event('resize'));
}

// Walk the DOM to find card element.
function recursive_walk(node, func) {
    var done = func(node) || node.nodeName == 'COMPACT-CUSTOM-HEADER';
    if (done) return true;
    if ('shadowRoot' in node && node.shadowRoot) {
      done = recursive_walk(node.shadowRoot, func);
      if (done) return true;
    }
    node = node.firstChild;
    while (node) {
      done = recursive_walk(node, func);
      if (done) return true;
      node = node.nextSibling;
    }
}

function element_style(config, element, shift) {
  let top = edit_mode ? 240 : 111;
  let options_style = element == options_btn ?
    'margin-right:-5px; padding:0;' : '';
  if (tabs_count.length > 1 && shift && !window.cch_disable) {
    element.style.cssText = config ?
      `z-index:1; margin-top:${top}px;${options_style}` :
      'display:none' ;
  } else if (!window.cch_disable){
    element.style.cssText = config ?
      '' :
      'display:none' ;
  } else {
    element.style.cssText = '';
  }
}

function remove_clock(config, element, parent) {
  if (window.cch_clock != config &&
      element.shadowRoot.getElementById('cch_clock') != null) {
    let clock_element = element.shadowRoot.getElementById('cch_clock');
    clock_element.parentNode.querySelector('iron-icon').style.cssText = '';
    if (config == 'options') {
      parent.querySelector('paper-icon-button').style.cssText = '';
    } else {
      parent.shadowRoot.querySelector('paper-icon-button').style.cssText = '';
    }
    if (config == 'notification') {
      notify_dot.style.cssText = '';
    }
    clock_element.parentNode.removeChild(clock_element);
  }
}

function show_user_agent() {
  if (card.querySelector('[id="cch_ua"]') != null) {
    if (window.cch_ua_display) {
      card.querySelector('[id="cch_ua"]').style.display = 'none';
      card.querySelector('[id="btn_ua"]').innerHTML = 'Show user agent';
      window.cch_ua_display = false;
    } else if (!window.cch_ua_display) {
      card.querySelector('[id="cch_ua"]').style.display = 'initial';
      card.querySelector('[id="btn_ua"]').innerHTML = 'Hide user agent';
      window.cch_ua_display = true;
    }
  }
}

function show_all_tabs() {
  if (!window.cch_tabs_display) {
    for (let i = 0; i < tabs_count.length; i++) {
      tabs_count[i].style.cssText = '';
    }
    window.cch_tabs_display = true;
    card.querySelector('[id="btn_tabs"]').innerHTML = 'Revert all tabs';
  } else if (window.cch_tabs_display) {
    for (let i = 0; i < tabs_count.length; i++) {
      if (window.cch_ua_views) {
        if (window.cch_ua_views.indexOf(String(i+1)) > -1) {
          tabs_count[i].style.cssText = '';
        } else {
          tabs_count[i].style.cssText = 'display:none;';
        }
      }
    }
    window.cch_tabs_display = false;
    card.querySelector('[id="btn_tabs"]').innerHTML = 'Show all tabs';
  }
}