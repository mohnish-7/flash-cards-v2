//////////////////////////////////////////////////////// Dashboard ////////////////////////////////////////////////////////////////

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
      <p class="score-details">{{deck_id}}</p>
    </strong>
  </div>
  <a id="practice-btn" href="">
  {{deck_id}}
    <button vue-on:click.native="activatePracticeBtn({{deck_id}})" type="submit" class="btn btn-primary practice-btn">Practice</button>
  </a>
  </div>
  `
})

let dashboard = new Vue({
  el: '#dashboard',
  delimiters: ['${', '}'],
  data() {
    return {
      username: u_name,
      decks: [],
      empty: false
    }
  },
  beforeMount: function() {
    console.log("beforeMount");
    fetch('http://127.0.0.1:5000/api/decks/' + u_name, {
        method: 'GET'
      })
      .then(response => response.json())
      .then(data => {
        console.log('Success:', data);
        for (let i = 0; i < data.length; i++) {
          this.decks.push(data[i]);
        }
        if (this.decks.length == 0) {
          this.empty = true;
        }
      })
      .catch((error) => {
        console.error('Error:', error);
      });
  },
  methods: {
    activatePracticeBtn: function(d_id) {

      document.getElementById("practice-btn").href = "/cards/" + d_id;
      alert('Im being called');
    }
  },
});
