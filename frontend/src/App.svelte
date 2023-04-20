<script lang="ts">
  import Button, { Label, Icon } from "@smui/button";
  import Handshake from "./assets/handshake.svelte";
  let data = fetch("/args").then((d) => d.json());
  let blur = function (ev) {
    ev.target.blur();
  };
</script>

<main>
  <h1>
    <a href="https://github.com/openai/evals">OpenAI</a>
    <Handshake />
    <a href="https://zenoml.com">Zeno</a>
  </h1>
  <h4>Explore the results of OpenAI evals all in one place...</h4>
  <!-- table with links to zeno sites. -->
  <div id="container">
    <div id="table-background">
      <table>
        <thead>
          <tr>
            <th>Evaluation</th>
            <th>Models</th>
            <th>Accuracy</th>
            <th>Events</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {#await data}
            <p>loading</p>
          {:then final_data}
            {#each final_data as d}
              {@const name = Object.keys(d)[0]}
              <tr>
                <td><div class="name-wrap">{name}</div> </td>
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
                    class="button-shaped-round"
                  >
                    <Icon class="material-icons">rocket</Icon>
                    <Label>Launch</Label>
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
    background-color: #dce3f6;
    width: 800px;
    padding: 20px;
    border-radius: 20px;
  }
  .name-wrap {
    border: 1px solid transparent;
    padding: 5px 10px;
    border-radius: 20px;
    background-color: #646cff;
    color: white;
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
    height: 64px;
  }
  tbody tr:hover {
    opacity: 1;
    background-color: #ededed;
  }
</style>
