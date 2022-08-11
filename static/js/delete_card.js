//////////////////////////////////////////////////////// New Deck ////////////////////////////////////////////////////////////////

let new_deck = new Vue({
  el: '#delete_card',
  delimiters: ['${', '}'],
  data() {
    return {
      card_title: "",
      deleted: false,
      error: ""
    }
  },
  methods: {
    del: function() {

      const data = {
        deck_id: d_id,
        card_title: this.card_title
      };
      if (this.card_title.length > 0) {
        fetch('http://127.0.0.1:5000/api/cards', {
            method: 'DELETE',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
          })
          .then(response => response.json())
          .then(data => {
            console.log('Success:', data);
            if (data.length > 0) {
              this.error = "";
              this.deleted = true;
            } else {
               this.error = "Card doesn't exist.";
            }

          })
          .catch((error) => {
            console.error('Error:', error);
          });
      } else {
            this.error = "Card title cannot be empty !"
      }


    }
  }
});
