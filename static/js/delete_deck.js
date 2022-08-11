//////////////////////////////////////////////////////// Delete Deck ////////////////////////////////////////////////////////////////

let delete_deck = new Vue({
  el: '#delete_deck',
  delimiters: ['${', '}'],
  data() {
    return {
      deck_name: "",
      created: false,
      error: ""
    }
  },
  methods: {
    del: function() {

      const data = {
        username: this.u_name,
        deck_name: this.deck_name
      };
      if (data.deck_name.length > 0) {
        fetch('http://127.0.0.1:5000/api/decks', {
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
              this.created = true;
            } else {
               this.error = "Deck doesn't exist.";
            }

          })
          .catch((error) => {
            console.error('Error:', error);
          });
      } else {
            this.error = "Deck Name cannot be empty !"
      }


    }
  }
});
