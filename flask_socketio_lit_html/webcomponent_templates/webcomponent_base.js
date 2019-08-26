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
        {% if property != 'index' %}
        this.{{ property }} = properties.{{ property }};
        {% endif %}
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
        Object.defineProperty(this, 'shadowRoot', {value: document,});
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
    createRenderRoot() {
        // https://stackoverflow.com/a/53195662
        // this is what overrides lit-element's behavior so that the contents don't render in shadow dom
        return this;
    };
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
    add_event() {
        var child = document.createElement('{{ component_name }}').newItem({
                username: document.getElementById('username').value, 
                email: document.getElementById('email').value
            })
            .then( (newItem) => {
                console.log("item", newItem.index, 'has been created');
        });
    }
    change_event() {
        index = document.getElementById('index').value;
        // This will not work with shadow root unless user-item shadow root is accessible
        var item = document.querySelectorAll('user-item[index="'+index+'"]')[0];
        item.username = document.getElementById('username').value;
        item.email = document.getElementById('email').value;
        item.set();
    };
    createRenderRoot() {
        // https://stackoverflow.com/a/53195662
        // this is what overrides lit-element's behavior so that the contents don't render in shadow dom
        return this;
    };
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
            </div>
            <button id="submit-button" class="btn btn-primary" @click="${ this.add_event }">Add</button>
        </form>
        <input id='index' value='2'>
        <mwc-button unelevated label="Change" @click="${ this.change_event }"></mwc-button>`;
    }
}
window.customElements.define('form-{{ component_name }}', Items);


class ItemsList extends LitElement {
    static get properties() {
        return {
            items: { 
                type: Array
            }
        }
    }
    constructor() {
        super();
        this.items = [];
        get('{{ base_url }}'+'/all').then(indexes => this.items = indexes.items);
        var items = this; // Capturing element in the update callback
        io_socket.on("{{ ioupdate }}", function(index_update) {
            if (!items.items.includes(index_update)) {
                console.log("upadated item:", items.items, "+", index_update);
                items.requestUpdate('items', [...items.items]);
                items.items.push(index_update);
                console.log("ioupdated:", items.items);
            }
        });
    };
    createRenderRoot() {
        return this;
    };
    render() {
        console.log("render:", this.items);
        return html`<ul>${this.items.map((index) => html`<li><{{ component_name }} index=${index}></{{ component_name }}></li>`)}</ul>`;
    }
}
window.customElements.define('ul-{{ component_name }}', ItemsList);
