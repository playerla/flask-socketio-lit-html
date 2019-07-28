import 'https://unpkg.com/@material/mwc-button@0.6.0/mwc-button.js?module';
import { LitElement, html, css } from 'https://unpkg.com/lit-element?module';

var io_socket = io()

const get = async (url) => { 
    const response = await fetch(url);
    if (response.status == 404)
        return null;
    return await response.json();
}
const post = async (url, json) => { 
    const response = await fetch(url, {
        method: 'POST',
        headers: new Headers({ "content-type": "application/json" }),
        body: JSON.stringify(json)
    });
    if (response.status == 404)
        return null;
    return await response.json();
}

class Item extends LitElement {
    static get properties() {
        return {
            {% for property in properties %}
            {{ property }}: {
                type: String
            },
            {% endfor %}
        }
    }
    _set(properties) {
        {% for property in properties %}
        this.{{ property }} = properties.{{ property }};
        {% endfor %}
    };
    async newItem(properties) {
        await post('{{ base_url }}', properties).then(json => this.index = json.index);
        console.log('new', this.index);
        return this;
    };
    set() {
        post('{{ base_url }}', {
        {% for property in properties %}
           {{ property }}: this.{{ property }},
        {% endfor %}
        })
    }
    _get() { 
        get('{{ base_url }}'+'/'+this.index).then(item => {
            if(item) {
                this._set(item);
                console.log(this.index, 'loaded:', item)
            }
            else
                console.log("undefined item ", this.index);
    })}
    updated(changedProperties) {
        if (changedProperties.has('index')) {
            // get the new item referenced by the primary key this.index
            this._get();
        }
    }
    constructor() {
        super();
        var element = this // Capturing element in the update callback
        io_socket.on("{{ ioupdate }}", function(index) {
            if (index == element.index)
                element._get();
        });
        this._get();
    };
    static get styles() {
        return css`
        {% block style %}
        {% endblock %}        
        `;
    }
    render() {
        return html`
        {% block render %}
        Your item <strong> ${ this.index } </strong> rendered here
        {% endblock %}
        `;
    };
}    
window.customElements.define('{{ component_name }}', Item);

class Items extends LitElement {
    static get properties() {
        return {
            items: { 
                type: Object
            }
        }
    }
    constructor() {
        super();
        this.items = {};
        var items = this; // Capturing element in the update callback
        io_socket.on("{{ ioupdate }}", function(index_update) {
            if (items.items[index_update] == undefined) {
                items.items[index_update] = document.createElement('{{ component_name }}');
                items.items[index_update].index = index_update;
                var $li = document.createElement('li');
                $li.appendChild(items.items[index_update])
                items.$ul.appendChild($li);            
            }
        });
    };
    firstUpdated() {
        this.$ul = this.shadowRoot.querySelector('ul');
    }
    add_event() {
        var child = document.createElement('{{ component_name }}').newItem({
                username: this.shadowRoot.getElementById('username').value, 
                email: this.shadowRoot.getElementById('email').value
            })
            .then( (newItem) => {
                console.log("item", newItem.index, 'has been created');
        });
    }
    change_event() { 
        var item = this.items[this.shadowRoot.getElementById('index').value];
        item.username = this.shadowRoot.getElementById('username').value;
        item.email = this.shadowRoot.getElementById('email').value;
        item.set();
    }
    render() {
        return html`
        <link rel="stylesheet" href="//cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.3.7/css/bootstrap.min.css" >
        <form onsubmit="return false;">
            <div class="form-group">
                <label for="username">Name</label>
                <input type="text" class="form-control input-lg" id="username" value="Name">
            </div>
            <div class="form-group">
                <label for="email">Email address</label>
                <input type="email" class="form-control input-lg" id="email" aria-describedby="emailHelp" value="name@example.com">
                <small id="emailHelp" class="form-text text-muted">We'll never share your email with anyone else.</small>
            </div>
            <button class="btn btn-primary" @click="${ this.add_event }">Add</button>
        </form>
        <ul>
        </ul>
        <input id='index' value='2'>
        <mwc-button unelevated label="Change" @click="${ this.change_event }"></mwc-button>`;
    }
}
window.customElements.define('ul-{{ component_name }}', Items);
