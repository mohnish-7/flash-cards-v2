//////////////////////////////////////////////////////// Delete Deck ////////////////////////////////////////////////////////////////

let edit_deck = new Vue({
  el: '#edit_deck',
  delimiters: ['${', '}'],
  data() {
    return {
      deck_name: "",
      new_name: "",
      updated: false,
      error: ""
    }
  },
  methods: {
    edit: function() {

      const data = {
        new_name: this.new_name,
        deck_name: this.deck_name
      };
      if (data.deck_name.length > 0 && data.new_name.length > 0) {
        fetch('http://127.0.0.1:5000/api/decks', {
            method: 'PUT',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
          })
          .then(response => response.json())
          .then(data => {
            console.log('Success:', data);
            if (Object.keys(data).length > 2) {
              this.error = "";
              this.updated = true;
            } else {
               this.error = data.error_message;
            }

          })
          .catch((error) => {
            console.error('Error:', error);
          });
      } else {
            this.error = "Deck Name or New Name cannot be empty !"
      }


    }
  }
});
