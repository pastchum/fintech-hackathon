export type PullDetailsType = {
  pullDetails: {
    title: string;
    description: string;
    link: string;
  };
};

export default function ArticleDisplay({ pullDetails }: PullDetailsType) {
  return (
    <a href={pullDetails.link} target="blank">
      <div className="p-2 border border rounded-xl shadow">
        <div className="text-xl font-bold p-2">{pullDetails.title}</div>
        <div className="text-slate-500">{pullDetails.description}</div>
      </div>
    </a>
  );
}
