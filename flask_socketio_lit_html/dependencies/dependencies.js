import {html, LitElement, css} from 'lit-element';

class MyElement extends LitElement {
  render() {
    return html`
      <p>Hello World</p>
      ${this.myProp}
    `;
  }
}
customElements.define('my-element', MyElement);
css("strong {color: blue;}");