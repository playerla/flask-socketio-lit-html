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
        return this;
    }
    _get() { 
        get('{{ base_url }}'+'/'+this.index).then(item => {
            if(item) {
                this._set(item);
                console.log(this.index, 'loaded')
            }
            else
                console.log("undefined item ", this.index);
    })}
    updated(changedProperties) {
        if (changedProperties.has('index')) {
            console.log(this.index, 'index updated')
            // get the new item referenced by the primary key this.index
            this._get();
        }
    }
    constructor() {
        super();
        var element = this // Capturing element in the update callback
        io_socket.on("{{ ioupdate }}", function(index) {
            if (index == element.index) {
                console.log('update for', index);
                element._get();
            }
        });
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
        var element = this // Capturing element in the update callback
        io_socket.on("{{ ioupdate }}", function(index_update) {
            if (element.items[index_update] == undefined)
                element._posted({index: index_update});
            get('{{ base_url }}'+'/all').then(json => {
                // Removing all removed items
                for (var index in element.items) {
                    if (!element.items[index].index in json.items) {
                        element.items[index].remove();
                        element.items[index] = undefined;
                    }
                }
            });
        });
    };
    firstUpdated() {
        this.$ul = this.shadowRoot.querySelector('ul');
    }
    _posted(properties) {
        var child = document.createElement('{{ component_name }}')._set(properties);
        this.items[properties.index] = child;
        var $li = document.createElement('li');
        $li.appendChild(child)
        this.$ul.appendChild($li);
    }
    _add({index=null}) {
        post('{{ base_url }}',
        {
            index: index, 
            username: this.shadowRoot.getElementById('username').value, 
            email: this.shadowRoot.getElementById('email').value
        });
    }
    _change() { 
        this._add({index:this.shadowRoot.getElementById('index').value}) ;
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
            <button class="btn btn-primary" @click="${ this._add }">Add</button>
        </form>
        <ul>
        </ul>
        <input id='index' value='2'>
        <mwc-button unelevated label="Change" @click="${ this._change }"></mwc-button>`;
    }
}
window.customElements.define('ul-{{ component_name }}', Items);
