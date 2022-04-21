/* 
    Custom Profile Card Component 
*/

class ProfileCard extends HTMLElement {
    constructor() {
      super();
    
    }
    
  
    
    //Runs each time customELement is inserted into the DOM
    connectedCallback() {
  
      //variables passed in from Django template language
      var title = this.attributes.title.value
      var subtitle = this.attributes.subtitle.value
      
  
      //Custom Html
      this.innerHTML = `
  
        <div class="card">
            <img src="img_avatar.png" alt="Avatar" style="width:100%">
            <div class="container">
                <h4><b>John Doe</b></h4>
                <p>Architect & Engineer</p>
            </div>
        </div>

      `
      
    }
}


/*  Registering the customElement.
    Passing it two arg.
    -DOMstring(what it will be rendered as in the index.html)
    -component class name   
*/
customElements.define('profile-card', ProfileCard);