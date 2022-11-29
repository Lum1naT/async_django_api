<script>
    import { onMount } from "svelte";
    import Continent from "./Continent.svelte";
    // define the data holding variable
    let continents;
  
  onMount(async () => {
      await fetch(`http://localhost:8000/sources/`)
        .then(r => r.json())
        .then(data => {
          continents = data;
        });
    })
  
</script>
<continents>
    {#if continents}
  {#each continents as continent }
    <ul>
      <li>    
        <Continent {continent} />
      </li>
    </ul>
  {/each}
{:else}
  <p class="loading">loading...</p>
{/if}
</continents>
<style>
    .loading {
      opacity: 0;
      animation: 0.4s 0.8s forwards fade-in;
    }
    @keyframes fade-in {
      from { opacity: 0; }
      to { opacity: 1; }
    }
    li {
      list-style-type: georgian;
    }
  </style>