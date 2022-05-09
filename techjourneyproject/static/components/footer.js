/*
  Custom Footer Component 
*/



class Footer extends HTMLElement {
    constructor() {
      super();
    
    }
    
  
    
    //Runs each time customELement is inserted into the DOM
    connectedCallback() {
  
      //variables passed in from Django template language
      //var href = this.attributes.href.value
      //var text = this.attributes.text.value
  
      //Custom Html
      this.innerHTML = `
  
        <footer>
          <nav class="footer-nav">
            <a href="/"><img src="/static/images/dreamwareLogo.png" height="18%" width="18%"></a>
  
            <ul class="nav-links">
              <ol><a href="/companies">Companies</a> </ol>
              <ol><a href="/">Team</a> </ol>           
            </ul>
  
          </nav>
        </footer>
      `
      
    }
  }
  
    
  /*  Registering the customElement.
      Passing it two arg.
      -DOMstring(what it will be rendered as in the index.html)
      -component class name   
  */
  customElements.define('footer-component', Footer);