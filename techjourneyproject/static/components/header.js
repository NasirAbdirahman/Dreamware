
/*
  Custom header Component 
*/
//const headerTemplate = document.createElement('template');


class Header extends HTMLElement {
  constructor() {
    super();
  
  }
  

  
  //Runs each time customELement is inserted into the DOM
  connectedCallback() {
    //Creating a shadow root for customElement - 'closed = inaccessible from external js
    //const shadowRoot = this.attachShadow({ mode: 'closed' });  

    //Append the shadowroot to the page
    //shadowRoot.appendChild(headerTemplate.content);

    //variables passed in from Django template language
    var loginHref = this.attributes.loginhref.value
    var loginText = this.attributes.logintext.value
    var joinHref = this.attributes.joinHref.value
    var joinText = this.attributes.joinText.value

    //Custom Html
    this.innerHTML = `

      <header>
        <nav class="nav-container">
          <a href="/"><img src="/static/images/dreamwareLogo.png" height="18%" width="18%"></a>

          <ul class="nav-links">
            <ol><a href="/"> Companies</a> </ol>
            <ol><a href="/"> Features</a> </ol>
            <ol><a href=${loginHref} class="authenticate-link"> ${loginText}</a> </ol>
            <ol><a class="nav-btn" href=${joinHref}>${joinText}</a></ol>
          </ul>

        </nav>
      </header>
    `
    
  }
}

  
/*  Registering the customElement.
    Passing it two arg.
    -DOMstring(what it will be rendered as in the index.html)
    -component class name   
*/
customElements.define('header-component', Header);