<script lang="ts">
  let data = fetch("/args").then((d) => d.json());
</script>

<main>
  <h1>OpenAI Evals Hub</h1>
  <h3>
    Explore the results of OpenAI evals using
    <a href="https://zenoml.com">Zeno</a>
  </h3>
  <!-- table with links to zeno sites. -->
  <div id="container">
    <!-- table with links to zeno sites. -->
    <table>
      <thead>
        <tr>
          <th>Evaluation</th>
          <th>View</th>
          <th>Models</th>
          <th>Accuracy</th>
          <th>data_column</th>
          <th>id_column</th>
          <th>batch_size</th>
          <th>samples</th>
        </tr>
      </thead>
      <tbody>
        {#await data}
          <p>loading</p>
        {:then final_data}
          {#each final_data as d}
            {@const name = Object.keys(d)[0]}
            {@const zeno = d[name]["zeno"]}
            {@const spec = d[name]["spec"]}
            <tr>
              <td><a href="/{name}/">{name}</a></td>
              <td>{zeno["view"]}</td>
              <td>{zeno["models"][0]}<br /> {zeno["models"][1]}</td>
              <td>{spec["accuracy"][0]}<br />{spec["accuracy"][1]}</td>
              <td>{zeno["data_column"]}</td>
              <td>{zeno["id_column"]}</td>
              <td>{zeno["batch_size"]}</td>
              <td>{zeno["samples"]}</td>
            </tr>
          {/each}
        {/await}
      </tbody>
    </table>
  </div>
</main>

<style>
  #container {
    margin: 50px 20px;
    display: flex;
    justify-content: center;
  }
  table {
    border-collapse: collapse;
    text-align: left;
  }
  table thead tr th {
    border-bottom: 0.5px solid grey;
  }
  table th,
  table td {
    border-bottom: 0.5px solid grey;
  }
  table th,
  table td {
    padding: 4px 20px;
  }
</style>
