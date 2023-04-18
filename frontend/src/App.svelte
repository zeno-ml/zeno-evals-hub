<script lang="ts">
  let data = fetch("/args").then((d) => d.json());
</script>

<main>
  <h1>OpenAI Evals Hub</h1>
  <h3>
    Explore the results of OpenAI evals using <a href="https://zenoml.com">Zeno</a>
  </h3>

  <!-- table with links to zeno sites. -->
  <table>
    <thead>
      <tr>
        <th>Evaluation</th>
      </tr>
    </thead>
    <tbody>
      {#await data}
        <p>loading</p>
      {:then final_data}
        {#each final_data as d}
          {@const name = Array.from(Object.keys(d))[0]}
          <tr>
            <td><a href="/{name}/">{name}</a></td>
          </tr>
        {/each}
      {/await}
    </tbody>
  </table>
</main>

<style>
</style>
