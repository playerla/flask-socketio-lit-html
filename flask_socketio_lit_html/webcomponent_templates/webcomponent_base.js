const io_socket = io()

const get_prop = (obj, key) => obj ? obj[key] : null;
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
        this._set(properties)
        await post('{{ base_url }}', properties).then(json => this.index = json.index);
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
        if (this.index)
            get('{{ base_url }}'+'/'+this.index).then(item => {
                if(item)
                    this._set(item);
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
        {% if config.WEBCOMPONENT_LIGHT_DOM == true %}
        Object.defineProperty(this, 'shadowRoot', {value: document,});
        {% endif %}
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
    };
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
        get('{{ base_url }}'+'/all').then(indexes => this.items = indexes.items);
        var items = this; // Capturing element in the update callback
        io_socket.on("{{ ioupdate }}", function(index_update) {
            if (!items.items.includes(index_update)) {
                items.requestUpdate('items', [...items.items]);
                items.items.push(index_update);
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
        return html`<ul>${this.items.map((index) => html`<li><{{ component_name }} index=${index}></{{ component_name }}></li>`)}</ul>`;
    }
}
window.customElements.define('ul-{{ component_name }}', ItemList);
