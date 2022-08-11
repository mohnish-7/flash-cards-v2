//////////////////////////////////////////////////////// Dashboard ////////////////////////////////////////////////////////////////

Vue.component('flash-deck', {
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

let dashboard = new Vue({
  el: '#dashboard',
  delimiters: ['${', '}'],
  data() {
    return {
      title: "Flash Cards"
    }
  }
});
