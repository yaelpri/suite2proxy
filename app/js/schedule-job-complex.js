add_experiment

let
  exp_count = 1;
  
  
function initialize_clickables() {
  Array
    .from(document
            .querySelectorAll('li'))
    .forEach(
      el => el.addEventListener('click', e => add_experiment(
        el.getAttribute('dir-date'),
        el.getAttribute('experiment')
      ))
    );
}


function launch_experiment_selection() {
  document
    .getElementById('selector')
    .classList
    .remove('invisible');
}


function cancel_experiment_selection() {
  document
    .getElementById('selector')
    .classList
    .add('invisible');
}


function add_experiment(dir_date, experiment) {
  const
    experiment_container = document.getElementById('experiments'),
    adder = document.getElementById('add'),
    div = document.createElement('div'),
    closer = document.createElement('a');

  div.classList.add('chained-experiment');
  div.classList.add('wiggler');

  div.setAttribute('exp-index', ++exp_count);
  div.setAttribute('exp-name', experiment);
  div.setAttribute('dir-date', dir_date);

  closer.classList.add('chained-experiment-closer');
  closer.classList.add('invisible');

  closer.addEventListener('click', (e) => {
    e.target.parentElement.remove();
    --exp_count;

    Array
      .from(document
              .getElementById('experiments')
              .children)
      .forEach((e, i) => {
        e.getAttribute('exp-index') && e.setAttribute('exp-index', i + 1);
      });
  });

  closer.addEventListener('mouseout', (e) => {
    e.target.classList.add('invisible');
    e.preventDefault();
  });

  div.addEventListener('mouseover', (e) => {
    try {
      e.target.children[0].classList.remove('invisible');
    } catch {}
  });

  div.appendChild(closer);

  adder.remove();
  experiment_container.appendChild(div);
  experiment_container.append(adder);

  cancel_experiment_selection();
}


function register_complex_job() {
  const
    settings_container = document.getElementById('settings'),
    experiment_container = document.getElementById('experiments'),
    experiment_divs = Array.from(experiment_container.children),
    experiments = experiment_divs
                    .filter((e) => e.getAttribute('exp-index'))
                    .map((e) => [
                        e.getAttribute('dir-date'),
                        e.getAttribute('exp-name')
                    ]),
    settings = {},
    xhr = new XMLHttpRequest();

  Array
    .from(settings_container.children)
      .filter(e => HTMLInputElement.name === e.constructor.name)
      .map(e => [e.name, e.value])
      .forEach(([name, value]) => {
        settings[name] = value;
      });

  const
    job = {
      experiments: experiments,
      settings: settings
    };

  xhr.open('POST', '/register-job-complex', true);
  xhr.onload = function () {
    alert('job registered;');
    window.location = '/';
  };

  xhr.send(JSON.stringify(job));
}
