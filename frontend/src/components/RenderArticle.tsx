export type Articles = {
  title: string;
  description: string;
  link: string;
};

type RenderArticlesProps = {
  Articles: Articles;
};

export default function RenderArticle({ Articles }: RenderArticlesProps) {
  return (
    <a href={Articles.link} target="blank">
      <div className="p-2 border border rounded-xl shadow transition-transform transform-scale-95 hover:transform-scale-100">
        <div className="text-xl font-bold p-2">{Articles.title}</div>
        <div className="text-slate-500">{Articles.description}</div>
      </div>
    </a>
  );
}
