<script lang="ts">
  import Button, { Icon, Label } from "@smui/button";
  let data = fetch("/args").then((d) => d.json());
  let blur = function (ev) {
    ev.target.blur();
  };
</script>

<main>
  <header>
    <h1>Zeno + OpenAI Evals</h1>
  </header>
  <div class="tagline">
    Use the <img class="open_ai" src="./build/zeno.png" alt="Zeno logo" />
    <b><a style:color="var(--logo)" href="https://github.com/zeno-ml/zeno/">Zeno</a></b>
    AI evaluation tool to compare the performance of models accross
    <img class="open_ai" src="./build/openai.svg" alt="OpenAI logo" />
    <a href="https://github.com/openai/evals">
      <b>OpenAI Evals</b>
    </a> tasks.
  </div>
  <br />
  <div class="tagline">
    Submit a PR to add new evals to this page!
    <iframe
      src="https://ghbtns.com/github-btn.html?user=zeno-ml&repo=zeno-evals-hub&type=fork&count=true"
      frameborder="0"
      scrolling="0"
      width="150"
      height="20"
      title="GitHub"
    />
  </div>
  <!-- table with links to zeno sites. -->
  <div id="container">
    <div id="table-background">
      <table>
        <thead>
          <tr>
            <th>evaluation</th>
            <th>description</th>
            <th>models</th>
            <th>accuracy</th>
            <th>instances</th>
            <th />
          </tr>
        </thead>
        <tbody>
          {#await data}
            <p>loading</p>
          {:then final_data}
            {#each final_data as d}
              {@const name = Object.keys(d)[0]}
              <tr>
                <td
                  ><a href={d[name]["link"]}><span class="name-wrap">{name}</span></a>
                </td>
                <td>{d[name]["description"]}</td>
                <td style:min-width="120px">
                  {#each d[name]["models"] as m}{m}<br />{/each}
                </td>
                <td>
                  {#each d[name]["accuracy"] as a}{a.toFixed(2)}%<br />{/each}
                </td>
                <td>
                  {d[name]["events"][0]}
                </td>
                <td>
                  <Button
                    on:mouseleave={blur}
                    on:focusout={blur}
                    href="/{name}/"
                    ripple={false}
                    variant="unelevated"
                    color="primary"
                  >
                    <Icon class="material-icons">rocket</Icon>
                    <Label>Open</Label>
                  </Button>
                </td>
              </tr>
            {/each}
          {/await}
        </tbody>
      </table>
    </div>
  </div>
</main>

<style>
  iframe {
    margin-left: 10px;
  }
  #container {
    margin: 50px 20px;
    display: flex;
    justify-content: center;
  }
  #table-background {
    width: 1100px;
    min-width: 900px;
    padding: 20px;
    border-radius: 20px;
  }
  .name-wrap {
    border: 1px solid transparent;
    border-radius: 10px;
    font-weight: 500;
    color: var(--logo);
  }
  .name-wrap:hover {
    color: var(--P2);
  }
  table {
    border-collapse: collapse;
    text-align: left;
    cursor: default;
    margin-left: auto;
    margin-right: auto;
  }
  table thead tr th {
    border-bottom: 0.5px solid grey;
  }
  table th,
  table td {
    padding: 4px 25px;
  }
  table td:first-child,
  table th:first-child {
    border-radius: 20px 0 0 20px;
  }
  table td:last-child,
  table th:last-child {
    border-radius: 0 20px 20px 0;
  }

  tbody:before {
    content: "@";
    display: block;
    line-height: 10px;
    text-indent: -99999px;
  }
  thead tr {
    color: #213547;
  }
  tbody tr {
    opacity: 0.9;
    height: 70px;
  }
  /* tbody tr:hover {
    opacity: 1;
    background-color: #ededed;
  } */
  .open_ai {
    width: 20px;
    margin-left: 5px;
  }
  .tagline {
    font-size: 18px;
    text-align: center;
    display: flex;
    justify-content: center;
    align-items: center;
  }
  .tagline b {
    margin-right: 5px;
    margin-left: 5px;
  }
  header {
    display: flex;
    align-items: center;
    justify-content: center;
  }
</style>
