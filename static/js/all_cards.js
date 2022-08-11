//////////////////////////////////////////////////////// Cards ////////////////////////////////////////////////////////////////

Vue.component('flash-card', {
  props: ['card_title', 'card_id', 'card_content'],
  data: function () {
    return {
      hreference: "#answer",

    }
  },
  template: `
  <div>
      <p class="question">{{card_title}}</p>
      <a  id="answer-btn" class="btn btn-primary q-btn ans-btn" data-bs-toggle="collapse" href="" role="button" aria-expanded="false" >
        Answer
      </a>
    <div>
      <div class="collapse answer" id="moni">
        <div class="card card-body explanation">
          {{card_content}}
        </div>
      </div>
    </div>
  </div>
  `,
  mounted: function () {
      this.$el.querySelector(".ans-btn").href = "#card"+this.card_id;
      this.$el.querySelector(".answer").id = "card"+this.card_id;
      console.log(this.data);
    }
})

let dashboard = new Vue({
  el: '#cards',
  delimiters: ['${', '}'],
  data() {
    return {
      d_name: deck_name,
      n: n_cards
    }
  },
  computed : {
    function () {
    console.log(d_name);
  }
}
});
