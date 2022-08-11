//////////////////////////////////////////////////////// Search Deck ////////////////////////////////////////////////////////////////
Vue.component('flash-card', {
  props: ['deck_name', 'score', 'num', 'last_review'],
  template: `
  <div>
  <strong>
    <h5 class="card-title">{{deck_name}}</h5>
  </strong>
  <div class="details">
    <strong>
      <div class="score">
        <h5 style="display:inline;">Latest Score: </h5>
      </div>
      <p class="score-details">{{score}}</p>
      <br>
      <div class="num-reviewed">
        <h5 style="display:inline;">Number of cards reviewed last time: </h5>
      </div>
      <p class="score-details">{{num}}</p>
      <br>
      <div class="last-review">
        <h5 style="display:inline;">Last reviewed on: </h5>
      </div>
      <p class="score-details">{{last_review}}</p>
    </strong>
  </div>
  </div>
  `
})
let search_deck = new Vue({
  el: '#search_deck',
  delimiters: ['${', '}'],
  data() {
    return {
      deck_name: "",
      searched: false,
      error: "",
      decks: []
    }
  },
  methods: {
    search: function() {

      const data = {
        username: u_name,
        deck_name: this.deck_name
      };
      if (data.deck_name.length > 0) {
        fetch('http://127.0.0.1:5000/api/decks/' + u_name, {
            method: 'GET'
          })
          .then(response => response.json())
          .then(data => {
            console.log('Success:', data);
            if (Object.keys(data).length > 0) {

              for (let i = 0; i < data.length; i++) {
                if (data[i].deck_name === this.deck_name) {
                  this.decks.push(data[i]);
                }
              }
              if (this.decks.length == 0) {
                this.error = "Deck not found.";
              } else {
                this.error = "";
                this.searched = true;
              }

            } else {
              this.error = "Deck not found.";
            }

          })
          .catch((error) => {
            console.error('Error:', error);
          });
      } else {
        this.error = "Deck Name cannot be empty !"
      }


    },
    activatePracticeBtn: function(d_id) {
      document.getElementById("practice-btn").href = "/cards/" + d_id;
    }
  }
});
