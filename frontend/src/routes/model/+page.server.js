// // export const prerender = true;
//
// import {readFileSync} from 'fs';
// import {resolve} from 'path';
//
// export async function load() {
//     const filePath = resolve('src/lib/model/Singapore Weather Prediction.svelte');
//     const htmlContent = readFileSync(filePath, 'utf-8');
//
//     console.log(htmlContent)
//
//     const adjustedHtmlContent = htmlContent.replace(
//         /src="(.*?)"/g,
//         (match, src) => {
//             if (!src.startsWith('http') && !src.startsWith('/')) {
//                 const relativeSrc =`src/lib/model/${src}`;
//                 return `src="${relativeSrc}"`;
//             }
//             return match;
//         }
//     );
//
//     return { htmlContent };
// }
//
