import 'https://unpkg.com/@material/mwc-button@0.6.0/mwc-button.js?module';
import { LitElement, html, css } from 'https://unpkg.com/lit-element?module';

const get = async (url) => { 
    const response = await fetch(url);
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
            index: { type: Number }
        }
    }
    constructor() {
        super();
        this.username = "undefined user";
        this.email = "undefined@example.com";
        this.socket = io();
        var element = this // Capturing element in the update callback
        this.socket.on('update', function() {
            get('user/'+element.id).then(user => {
                if(user) {
                    element.username = user.username;
                    element.email = user.email;
                }
                else
                    console.log("undefined user "+element.id)
            })
        });
    };
    _add() {
        this.socket.emit('add', 
            {
                username: this.shadowRoot.getElementById('username').value, 
                email: this.shadowRoot.getElementById('email').value
            })
    };
    render() {
        return html`
            <input id='username' value='username'>
            <input id='email' value='email'>
            <mwc-button unelevated label="Add" @click="${ this._add }"></mwc-button>
            <ul>
                <li><strong>${ this.username }</strong> ${ this.email }</li>
            </ul>
            `;
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
        this.socket = io();
        var element = this // Capturing element in the update callback
        this.socket.on('update', function() {
            get('users').then(users => element.users = users.list )
        });
    };
    render() {
        return html`
        <ul>
            ${this.users.map((u) => html`<li><strong>${ u.username }</strong> ${ u.email }</li>`)}
        </ul>`;
    }
}
window.customElements.define('ul-users', Users);
