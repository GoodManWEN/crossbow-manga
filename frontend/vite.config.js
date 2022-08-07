import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import Components from "unplugin-vue-components/vite";
import { ElementPlusResolver } from "unplugin-vue-components/resolvers";
import { resolve } from "path";

// https://vitejs.dev/config/
export default defineConfig({
	plugins: [
		vue(),
		Components({
			resolvers: [
				ElementPlusResolver({
					importStyle: "sass",
				}),
			],
		}),
	],
	server: { port: 7000 },
	resolve: {
		alias: {
			"~/": `${resolve(__dirname, "src")}/`,
			"@": resolve(__dirname, "src"),
		},
		// why remove it , look for https://github.com/vitejs/vite/issues/6026
		// extensions: ['.js', '.ts', '.jsx', '.tsx', '.json', '.vue', '.mjs']
	},
	css: {
		preprocessorOptions: {
			//define global scss variable
			scss: {
				additionalData: `@use "~/styles/index.scss" as *;`,
				// additionalData: `@import "@/styles/variables.scss";`,
			},
		},
	},
});
