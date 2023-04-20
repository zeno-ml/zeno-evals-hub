<script lang="ts">
  import Button, { Icon, Label } from "@smui/button";
  let data = fetch("/args").then((d) => d.json());
  let blur = function (ev) {
    ev.target.blur();
  };
</script>

<main>
  <header>
    <h1>Evals Hub</h1>
  </header>
  <div class="tagline">
    Explore and compare the results of
    <img class="open_ai" src="./build/openai.svg" alt="OpenAI logo" />
    <a href="https://github.com/openai/evals">
      <b>OpenAI Evals </b>
    </a>
    using
    <img class="open_ai" src="./build/zeno.png" alt="Zeno logo" />
    <b><a href="https://github.com/zeno-ml/zeno/stargazers">Zeno</a></b>
  </div>
  <!-- table with links to zeno sites. -->
  <div id="container">
    <div id="table-background">
      <table>
        <thead>
          <tr>
            <th>evaluation</th>
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
                <td><a href="#"><span class="name-wrap">{name}</span></a> </td>
                <td>
                  {#each d[name]["models"] as m}{m}<br />{/each}
                </td>
                <td>
                  {#each d[name]["accuracy"] as a}{a}%<br />{/each}
                </td>
                <td>
                  {#each d[name]["events"] as e}{e}<br />{/each}
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
  #container {
    margin: 50px 20px;
    display: flex;
    justify-content: center;
  }
  #table-background {
    width: 900px;
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
