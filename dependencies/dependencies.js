import {html, LitElement, css} from 'lit-element';
import { repeat } from 'lit-html/directives/repeat.js'

class MyElement extends LitElement {
  render() {
    return html`
      <p>Hello World</p>
      ${repeat(MyElement,()=>null, html``)}
      ${this.myProp}
    `;
  }
}
customElements.define('my-element', MyElement);
css("strong {color: blue;}");