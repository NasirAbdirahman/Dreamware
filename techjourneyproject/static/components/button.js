
/*
  Custom Button Component 
*/


class Button extends HTMLElement {
    constructor() {
      super();
    
    }
    
  
    
    //Runs each time customELement is inserted into the DOM
    connectedCallback() {
  
      //variables passed in from Django template language
      var href = this.attributes.href?.value || ""
      var text = this.attributes.text.value || null

  
      //Custom Html that renders
      this.innerHTML = `<a class="btn-main" href=${href}>${text}</a> `
      
    }
  }
  
    
  /*  Registering the customElement.
      Passing it two arg.
      -DOMstring(what it will be rendered as in the index.html)
      -component class name   
  */
  customElements.define('button-component', Button);