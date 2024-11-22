<script>
    export let width = "100%"; // Default to full width
    export let color = "#333"; // Default gray color
    export let thickness = "1px"; // Default thickness
    export let margin = "0"; // Default top and bottom spacing
</script>

<div class="line" style="width: {width}; background-color: {color}; height: {thickness}; margin: {margin};"></div>

<style>
    .line {
        display: block;
		border-bottom: 8px solid #333;
    }
</style>
