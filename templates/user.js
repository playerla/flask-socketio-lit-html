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

class User extends LitElement {
    static get properties() {
        return {
            username: { 
                type: String,
            },
            email: { 
                type: Boolean,
            },
            index: { 
                type: Number,
            }
        }
    }
    _get() { 
        get('user/'+this.index).then(user => {
            if(user) {
                this.username = user.username;
                this.email = user.email;
                console.log(this.index, 'loaded')
            }
            else
                console.log("undefined user ", this.index);
    })}
    updated(changedProperties) {
        if (changedProperties.has('index')) {
            console.log(this.index, 'index updated')
            // get the new user referenced by the primary key this.index
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
    render() {
        return html`<strong>${ this.username }</strong> ${ this.email }`;
    };
}    
window.customElements.define('user-item', User);

class Users extends LitElement {
    static get properties() {
        return {
            users: { 
                type: Array
            }
        }
    }
    constructor() {
        super();
        this.users = [];
        var element = this // Capturing element in the update callback
        io_socket.on("{{ ioupdate }}", function() {
            get('users').then(json => { 
                element.users = json.users 
            });
        });
    };
    _post({index=null}) {
        post('user', 
        {
            index: index, 
            username: this.shadowRoot.getElementById('username').value, 
            email: this.shadowRoot.getElementById('email').value
        });
    }
    _change() { 
        this._post({index:this.shadowRoot.getElementById('index').value}) ;
    }
    render() {
        return html`
        <input id='username' value='username'>
        <input id='email' value='email'>
        <mwc-button unelevated label="Add" @click="${ this._post }"></mwc-button>
        <input id='index' value='2'>
        <mwc-button unelevated label="Change" @click="${ this._change }"></mwc-button>
        <ul>
           ${ this.users.map((index) => html`<li><user-item index="${ index }" ></user-item></li>`) }
        </ul>`;
    }
}
window.customElements.define('ul-users', Users);
