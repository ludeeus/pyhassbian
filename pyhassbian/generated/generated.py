"""Static texts."""
STYLE = """
<head>
    <title>Hassbian Manager</title>
    <link rel="shortcut icon" href="/static/package.ico" />
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
    <link href='http://fonts.googleapis.com/css?family=Roboto' rel='stylesheet' type='text/css'>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css">
    <link rel="stylesheet" href="static/style.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
    <script src="static/action.js"></script>
</head>
"""

HEADER = """
<header>
  <nav>
    <div class="nav-wrapper">
      <a href="/" class="brand-logo">&nbsp;&nbsp;&nbsp;Hassbian Manager</a>
      <ul id="nav-mobile" class="right hide-on-med-and-down">
        <li><a href="/">Suites</a></li>
        <li><a href="/log">Log</a></li>
      </ul>
    </div>
  </nav>
</header>
"""

CARD = """
  <div class="row">
    <div class="col s12">
      <div class="card blue-grey darken-1">
        <div class="card-content white-text" id="{title}">
          <span class="card-title">{title}</span>
          <p>{content}</p>
        </div>
        <div class="card-action">
          <a href="{more}">More info</a>
        </div>
      </div>
    </div>
  </div>
"""

SUITE = """
  <div class="row suiterow">
    <div class="col s12">
      <div class="card blue-grey darken-1">
        <div class="card-content white-text" id="{title}">
          <span class="card-title">{title}</span>
          <p>{content}</p>
        </div>
        <div class="card-action">
          {buttons}
        </div>
      </div>
    </div>
  </div>
"""

LOG = """
  <div class="row">
    <div class="col s12">
      <div class="card blue-grey darken-1">
        <div class="card-content white-text">
          <p>{}</p>
        </div>
        <div class="card-action">
          <a href="/log">Refresh</a>
        </div>
      </div>
    </div>
  </div>
</main>
"""
