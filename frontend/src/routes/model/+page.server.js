import {readFileSync} from 'fs';
import {resolve} from 'path';

export async function load() {
    const filePath = resolve('src/lib/model/Singapore Weather Prediction.html');
    const htmlContent = readFileSync(filePath, 'utf-8');

    // Adjust the URLs of iframes and images to use absolute paths
    const adjustedHtmlContent = htmlContent.replace(
        /src="(.*?)"/g,
        (match, src) => {
            if (!src.startsWith('http') && !src.startsWith('/')) {
                const relativeSrc =`src/lib/model/${src}`;
                return `src="${relativeSrc}"`;
            }
            return match;
        }
    );

    return { htmlContent: adjustedHtmlContent };
}

