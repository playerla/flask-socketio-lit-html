const io_socket = io()

const get_prop = (obj, key) => obj ? obj[key] : null;
const api = async (endpoint, parameters= {} ) => {
    try {
        let response = await fetch(endpoint, parameters);
        return response.json().catch(() => console.error('Bad response'));
    }
    catch(e) {
        console.error("A network error occured");
        throw e
    };
}
const get = async (index) => {
    return api('{{ base_url }}/'+index).then(item => {
        if (item)
            sessionStorage.setItem('{{ component_name }}.'+item.index, JSON.stringify(item));
        return item;
    });;
}
const post = async (item) => {
    return api('{{ base_url }}', {
            method: 'POST',
            headers: new Headers({ "content-type": "application/json" }),
            body: JSON.stringify(item)
        }).then(json => {
            item.index = json.index;
            sessionStorage.setItem('{{ component_name }}.'+json.index, JSON.stringify(item));
            return json;
        });
}
const del = async (index) => {
    sessionStorage.removeItem('{{ component_name }}.'+index);
    return api('{{ base_url }}/'+index, {
        method: 'DELETE',
    });
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
        this._set(properties)
        await post(properties).then(json => this.index = json.index);
        return this;
    };
    set() {
        post({
        {% for property in properties %}
           {{ property }}: this.{{ property }},
        {% endfor %}
        })
    }
    _get() {
        if (this.index) {
            const cached_json = JSON.parse(sessionStorage.getItem('{{ component_name }}.'+this.index))
            if (cached_json)
                this._set(cached_json)
            get(this.index).then(item => {
                if(item)
                    this._set(item);
                else
                    console.log("undefined item ", this.index);
            })
        }
    }
    delete_() {
        if (this.index) {
            if (!this.hasOwnProperty('_deleted'))
                del(this.index)
            if (this.parentNode)
                this.parentNode.removeChild(this);
    }
}    updated(changedProperties) {
        if (changedProperties.has('index')) {
            // get the new item referenced by the primary key this.index
            this._get();
        }
    }
    constructor() {
        super();
        {% if config.WEBCOMPONENT_LIGHT_DOM == true %}
        Object.defineProperty(this, 'shadowRoot', {value: document,});
        {% endif %}
        var element = this // Capturing element in the update callback
        io_socket.on("{{ ioupdate }}", function(index) {
            if (index == element.index)
                element._get();
        });
        io_socket.on("{{ iodelete }}", function(index) {
            if (index == element.index) {
                element._deleted = true
                element.delete_();
            }
        });
        this._get();
    };
    static get styles() {
        return css`
        {% block style %}
        {% endblock %}
        `;
    }
    {% macro WEBCOMPONENT_LIGHT_DOM() %}
    {% if config.WEBCOMPONENT_LIGHT_DOM == true %}
    createRenderRoot() {
        return this;
    };
    {% endif %}
    {% endmacro %}
    {{ WEBCOMPONENT_LIGHT_DOM() }}
    render() {
        return html`
        {% block render %}
        Your item <strong> ${ this.index } </strong> rendered here
        You must define webcomponent_base's block 'render'
        {% endblock %}
        `;
    };
}
window.customElements.define('{{ component_name }}', Item);

class ItemForm extends Item {
    add_event() {
        let child = document.createElement('{{ component_name }}');
        child.newItem({
            {% for property in properties %}
            {% if property != 'index' %}
                {{ property }}: get_prop(this.shadowRoot.getElementById('{{ property }}'), 'value'),
            {% endif %}
            {% endfor %}
            })
        .then( (newItem) => {
            console.log("item", newItem.index, 'has been created');
        });
        this.dispatchEvent(new CustomEvent('item-created', {detail: child}))
    }
    change_event() {
        {% for property in properties %}
        this.{{ property }} = get_prop(this.shadowRoot.getElementById('{{ property }}'), 'value'),
        {% endfor %}
        this.set();
        this.index = undefined
    };
    static get styles() {
        return [css`
        {% block style_form %}
        {% endblock %}
        `, super.styles];
    }
    render() {
        return html`
        {% block form %}
        <form onsubmit="return false;">
            <input type="text" id="yourProperty" value="propertyValue">
            <button @click="${ this.add_event }">Add</button>
            <input id='index' value='2'>
            <button @click="${ this.change_event }">Change</button>
        </form>
        You must define webcomponent_base's block 'form'
        {% endblock %}
        `;
    }
}
window.customElements.define('form-{{ component_name }}', ItemForm);


class ItemList extends LitElement {
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
        api('{{ base_url }}/all').then(indexes => this.items = indexes.items);
        var items = this; // Capturing element in the update callback
        io_socket.on("{{ ioupdate }}", function(index_update) {
            if (!items.items.includes(index_update)) {
                items.requestUpdate('items', [...items.items]);
                items.items.push(index_update);
            }
        });
        io_socket.on("{{ iodelete }}", function(index_deleted) {
            if (items.items.includes(index_deleted)) {
                items.requestUpdate('items', [...items.items]);
                items.items.splice(items.items.indexOf(index_deleted), 1);
            }
        });
    };
    static get styles() {
        return css`
        {% block list_style %}
        li {
            list-style: none;
        }
        {% endblock %}
        `;
    }
    {{ WEBCOMPONENT_LIGHT_DOM() }}
    render() {
        return html`<ul>${repeat(this.items, (index) => index, (index) => html`<li><{{ component_name }} index=${index}></{{ component_name }}></li>`)}</ul>`;
    }
}
window.customElements.define('ul-{{ component_name }}', ItemList);
