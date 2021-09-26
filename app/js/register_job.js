
function register_job() {

  const
    settings = {},
    all_forms = document.querySelectorAll('form'),
    selected_forms = Array.from(all_forms).filter((form) => form.children[0].checked);

  selected_forms.forEach(
    selected_form => Array
     .from(selected_form
             .children[1]
             .children)
     .filter(e => HTMLInputElement.name === e.constructor.name)
     .map(e => [e.name, e.value])
     .forEach(([name, value]) => {
       const
         data_file = selected_form.getAttribute('data-file');

       if (undefined === settings[data_file])
         settings[data_file] = {};

       settings[data_file][name] = value;
     })
  );

  if (selected_forms.length) {
    const
      job = {[selected_forms[0].getAttribute('dir-exp')]: settings},
      xhr = new XMLHttpRequest();

    xhr.open('POST', '/register-job', true);
    xhr.onload = function () {
      alert('job registered;')
      window.location = '/';
    };
    xhr.send(JSON.stringify(job));
  } else {
    alert('selection looks empty;');
  }
}