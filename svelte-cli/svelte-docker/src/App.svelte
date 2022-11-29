<script>
	import { onMount } from "svelte";
	import Continent from "./Continent.svelte";
	import Continents from "./Continents.svelte";
	let continents;
	let continent;
  </script>
  
  <h1>The Seven Continents Svelte App</h1>
  <main>
	  <Continents {continents} />
  </main>

<style>
	main {
		text-align: center;
		padding: 1em;
		max-width: 240px;
		margin: 0 auto;
	}


	@media (min-width: 640px) {
		main {
			max-width: none;
		}
	}
</style>